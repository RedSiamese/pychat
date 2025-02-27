"""
使用老流程(大分区小分区逐级归并流程)和csv数据进行聚档
大体流程为：
1. 读取一个目录，遍历子目录，获取所有csv数据，构建一个分区数据列表，类型为list[list[str]]（例如[["./0-0.csv", "./0-1.csv", "./0-2.csv"], ["./1-0.csv", "./1-1.csv", "./1-2.csv"], ...]），第一层list表示大分区，第二层表示每个大分区的小分区抓拍集所包含的抓拍数据路径。
2. 遍历每个大分区，将大分区中的每个小分区数据进行batch聚档操作，分别生成档案集，可以用线程池多线程处理。
3. 进行完成后，分别将每个大分区的小分区聚档得到的档案集用oc接口进行合档，合档之后结合合档结果调用check_multi接口进行离线合档，生成每个大分区档案集。
4. 将所有大分区档案集使用进行合档和离线合档操作。在每次做这个操作前先将人体模态档案隐藏，完成操作后将人体模态还原。生成最终档案

主要使用接口：
pycluster.cluster_hdl
pypic.pb_input_csv, pypic.get_level, 
pydossier.batch, pydossier.oc, pydossier.check_multi, pydossier.shadow, pydossier.shadow_restore, pydossier.save_small, pydossier.load_small
"""
def main():
    from concurrent.futures import ThreadPoolExecutor as thread_pool
    import os, functools, argparse, functools 

    import pycluster2x
    from pycluster2x import pycluster, pydossier, pypic, pycache

    parser = argparse.ArgumentParser(description='cluster old process')
    parser.add_argument('--data_path', help='data path, like --data_path /data/291223/data/shucheng/ffe221_reid115/', nargs='?')
    parser.add_argument('--result_host', default='', help='result host, like --result_host 10.12.76.155', nargs='?')
    parser.add_argument('--result_port', default=-1, help='result port, like --result_port 23508', nargs='?', type=int)
    parser.add_argument('--task', default='', help='task id, like --task 3035', nargs='?')
    parser.add_argument('--result_path', default='./result/', help='save result path, like --result_path ./result/, \'./result/\' is default', nargs='?')
    parser.add_argument('--result_name', default='', help='result name on server, like --result_name result , \'\' is default', nargs='?')
    parser.add_argument('--device_id', default=['0'], help='device id when running, like --device_id 0 , 0 is default', nargs='+')
    parser.add_argument('--data_cache', default='./data_cache/', help='device id when running, like --data_cache ./data_cache/ , \'./data_cache/\' is default', nargs='?')
    parser.add_argument('--oc_size', default=2000000, help='oc max size to distributed, like --oc_size 2000000', nargs='?', type=int)
    args = parser.parse_args()

    cache = pycache.cluster_data_cache(args.data_cache)

    default_cfg = pycluster.default_cfg()
    default_cfg['data_cache'] = args.data_cache
    default_cfg['device_id'] = args.device_id[0]

    # ##################################################################################
    # download data
    # ##################################################################################

    def has_csv(paths:'list[str]')->bool:
        for i in paths:
            if '.csv' in i:
                return True
        return False

    csvlist_all = []
    for a,b,c in os.walk(args.data_path):
        if has_csv(c):
            csvlist_all.append(list(map(lambda x: f"{a}/{x}", c)))
    big_partition_num = len(csvlist_all)

    thp_down = thread_pool(5)
    futures = []
    for csvlist in csvlist_all:
        for csv_path in csvlist:
            part = csv_path
            if not cache.contains(str(part)):
                def download(part):
                    pb = pypic.pb_input_csv(part)
                    print(f"download {part} finished")
                    return part, pb
                futures.append(thp_down.submit(download, part))
    for future in futures:
        part, pb = future.result()
        cache.save(pb, part)
        print(f"save {part} finished")

    oc_thread_num = max(int(1 * args.oc_size / (cache.size() / big_partition_num / 2.5)), 1)
    bp_thread_num = max(int(cache.size() * 64 / big_partition_num / 2.5 / args.oc_size), 1)
    print('big_partition_num', big_partition_num, 'oc_thread_num', oc_thread_num, 'bp_thread_num', bp_thread_num)

    # ##################################################################################
    # process
    # ##################################################################################

    def batch(partition:str, res_path:str):
        try:
            path = f"{res_path}/{partition}/"
            if not os.path.exists(path+"cfg.json"):
                print('batch', path)
                pb = cache.get_partition(partition)
                alg = pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], default_cfg)
                dossier_tmp = pydossier.dossier(alg)
                pb.get_level(alg)
                illegal = pb.get_level(-127, 0)
                print(f"{partition} illegal num:", illegal)
                pb = pb.get_level(0, 127)
                dossier_tmp.batch(pb)
                dossier_tmp.save_small(path)
            return path
        except (pycluster.cluster_logic_error, pycluster.cluster_div_mem_error) as err:
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path+"err.log", "w") as f:
                import traceback
                stack_info = traceback.format_exc()
                f.write(f"partition {partition}\n")
                f.write(f"{stack_info}\n")
            raise RuntimeError(f"partition {partition}: {err}")

    # 包含oc接口调用的子任务
    # batch_thread_pool = thread_pool(40)
    def one_day(big_partition_id:int, res_path:str):
        try:
            csvs = csvlist_all[big_partition_id]
            path = f"{res_path}/{big_partition_id}/"
            if not os.path.exists(path+"cfg.json"):
                thp_run = thread_pool(bp_thread_num)
                dossier_all = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], default_cfg))
                sub_partition_num = len(csvlist_all[big_partition_id])
                future_list = [thp_run.submit(pycluster2x.strack_dec(batch, f"batch partition: {csvs[i]}"), f"{csvs[i]}", path) for i in range(0, sub_partition_num)]      # 小分区数量
                for future in future_list:
                    dossier_tmp_path = future.result()
                    dossier_tmp = pydossier.load_small(dossier_tmp_path, default_cfg)
                    oc_res = dossier_all.oc(dossier_tmp)
                    dossier_all.check_multi(dossier_tmp, oc_res, "ex_fuse_oc|assisted_oc")
                    # dossier_all.save(f"{res_path}/{big_partition_id}_0_{i}/")
                dossier_all.save_small(path)
            return path
        except (pycluster.cluster_logic_error, pycluster.cluster_div_mem_error) as err:
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path+"err.log", "w") as f:
                import traceback
                stack_info = traceback.format_exc()
                f.write(f"partition {big_partition_id} part {part}\n")
                f.write(f"{stack_info}\n")
                dossier_all.save_small(path+"dossier_base")
                dossier_tmp.save_small(path+"dossier_other")
            raise RuntimeError(f"partition {big_partition_id} part {part}: {err}")
        
    def all_data(res_path:str, big_partition_num:int):
        try:
            thp_run = thread_pool(oc_thread_num)
            dossier_all = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], default_cfg))
            dossier_all.set_cfg("face_cluster_feat_threshold","0.95")
            future_list = [thp_run.submit(pycluster2x.strack_dec(one_day, f"oc partition: {i}"), i, res_path) for i in range(0, big_partition_num)]     # 大分区数量
            for future in future_list:
                dossier_tmp_path = future.result()
            for future in future_list:
                dossier_tmp_path = future.result()
                dossier_tmp = pydossier.load_small(dossier_tmp_path, default_cfg)
                oc_res = dossier_all.oc(dossier_tmp)
                dossier_all.check_multi(dossier_tmp, oc_res, "self_check|ex_fuse_oc")
                dossier_all.shadow()
                # dossier_all.save(f"{res_path}/all0_{i}/")
            dossier_all.shadow_restore()
            # dossier_all.tidy_up()
            dossier_all.save_small(f"{res_path}/all/")
            return dossier_all
        except (pycluster.cluster_logic_error, pycluster.cluster_div_mem_error) as err:
            if not os.path.exists(f"{res_path}/all/"):
                os.mkdir(f"{res_path}/all/")
            with open(f"{res_path}/all/err.log", "w") as f:
                import traceback
                stack_info = traceback.format_exc()
                f.writel(f"partition all part {part}\n")
                f.write(f"{stack_info}\n")
                dossier_all.save_small(f"{res_path}/all/dossier_base/")
                dossier_tmp.save_small(f"{res_path}/all/dossier_other/")
            raise RuntimeError(f"partition all part {part}: {err}")


    with pycluster2x.record(f"{args.result_path}/info_record.json"):
        dossier_all = all_data(args.result_path, big_partition_num)
    if args.result_host != '':
        try:
            import pydata_service
            res_service = pydata_service.result_service(args.result_host, args.result_port, args.task)
            table = res_service.get_result_table(args.result_name)
            table.upload(dossier_all.get_rid2pid())
        except:
            print("Result Upload FAILD!")
