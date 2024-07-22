import os, sys
import pandas as pd
import shutil
import time
from bmtk.simulator import pointnet

FLO_parameters = {'instants_attack':[10],'v_increment':[5,10,20,30,551], 'n_neurons':[50,100,200,300,400,450]}
JAM_parameters = {'init_attack':1000,'end_attack':1500,'n_neurons':[50,100,200,300,400,450]}
typ_attack = " "
n_exec = 10
def type_attack():
    global typ_attack
    with open("/home/victoria/type_attack.txt", 'r') as file:
        line = file.readline()
        attack = line.split(":")
        attack_ = attack[1]
        attack_ = attack_[:3]
        if attack_ == "FLO":
            typ_attack = "FLO"
        elif attack_ == "JAM":
            typ_attack = "JAM"    

def run(config_file):
    
    configure = pointnet.Config.from_json(config_file)
    configure.build_env()
 
    graph = pointnet.PointNetwork.from_config(configure)
    sim = pointnet.PointSimulator.from_config(configure, graph)
    sim.run()

if __name__ == '__main__':
    type_attack()
    folder_path_FLO = "/home/victoria/spikes_results_FLO"
    folder_path_JAM = "/home/victoria/spikes_results_JAM"
    folder_path_normal = "/home/victoria/spikes_results_normal"

    if typ_attack == "FLO":

        for instant in FLO_parameters["instants_attack"]:
            for voltage in FLO_parameters["v_increment"]:
                for neurons in FLO_parameters["n_neurons"]:
                    for exec in range(n_exec):
                        with open("/home/victoria/FLO_attributes.txt", 'w') as flo_file:
                            flo_file.write('instants_attack:{}\n'.format(instant))
                            flo_file.write('v_increment:{}\n'.format(voltage))
                            flo_file.write('n_neurons:{}\n'.format(neurons))

                        run('config.simulation.json')
                        
                        df_spikes = pd.read_csv("./output/_spikes.csv", delimiter=" ")
                        df_spikes = df_spikes.drop(['population'], axis = 1)
                        df_spikes['attack'] = 'FLO'
                        df_spikes['instants_attack'] = instant
                        df_spikes['voltage'] = voltage
                        df_spikes['n_neurons'] = neurons
                        df_spikes['n_exec'] = exec

                        df_spikes = df_spikes.reindex(columns=['attack','instants_attack','voltage','n_neurons','n_exec','timestamps','node_ids'])

                        if not os.path.exists(folder_path_FLO):
                            os.makedirs(folder_path_FLO)
                            df_spikes.to_csv(folder_path_FLO+"/FLO_"+str(instant)+"ms_"+str(voltage)+"mv_"+str(neurons)+"neurons_"+str(exec)+".csv")
                        else:
                            df_spikes.to_csv(folder_path_FLO+"/FLO_"+str(instant)+"ms_"+str(voltage)+"mv_"+str(neurons)+"neurons_"+str(exec)+".csv")

    elif typ_attack == "JAM":

        for neurons in JAM_parameters["n_neurons"]:
            for exec in range(n_exec):
                
                with open("/home/victoria/JAM_attributes.txt", 'w') as jam_file:
                    jam_file.write('init_attack:{}\n'.format(JAM_parameters["init_attack"]))
                    jam_file.write('end_attack:{}\n'.format(JAM_parameters["end_attack"]))
                    jam_file.write('n_neurons:{}\n'.format(neurons))

                run('config.simulation.json')
                    
                df_spikes = pd.read_csv("./output/_spikes.csv", delimiter=" ")
                df_spikes = df_spikes.drop(['population'], axis = 1)
                df_spikes['attack'] = 'JAM'
                df_spikes['init_attack'] = JAM_parameters["init_attack"]
                df_spikes['end_attack'] = JAM_parameters["end_attack"]
                df_spikes['n_neurons'] = neurons
                df_spikes['n_exec'] = exec

                df_spikes = df_spikes.reindex(columns=['attack','init_attack','end_attack','n_neurons','n_exec','timestamps','node_ids'])

                if not os.path.exists(folder_path_JAM):
                    os.makedirs(folder_path_JAM)
                    df_spikes.to_csv(folder_path_JAM+"/JAM_init"+str(JAM_parameters["init_attack"])+"ms_end"+str(JAM_parameters["end_attack"])+"ms_"+"mv_"+str(neurons)+"neurons_"+str(exec)+".csv")
                else:
                    df_spikes.to_csv(folder_path_JAM+"/JAM_init"+str(JAM_parameters["init_attack"])+"ms_end"+str(JAM_parameters["end_attack"])+"ms_"+"mv_"+str(neurons)+"neurons_"+str(exec)+".csv")
             
    else:
        run('config.simulation.json')

    if typ_attack == "FLO":
        file_list = os.listdir(folder_path_FLO)
        df_list = []

        for file in file_list:
            file_path = os.path.join(folder_path_FLO, file)
            if os.path.isfile(file_path):
                df = pd.read_csv(file_path)
                df_list.append(df)

        concatenated_df = pd.concat(df_list)
        concatenated_df.to_csv(folder_path_FLO + '/result_FLO.csv', index=False)

    elif typ_attack == "JAM":
        file_list = os.listdir(folder_path_JAM)
        df_list = []

        for file in file_list:
            file_path = os.path.join(folder_path_JAM, file)
            if os.path.isfile(file_path):
                df = pd.read_csv(file_path)
                df_list.append(df)

        concatenated_df = pd.concat(df_list)
        concatenated_df.to_csv(folder_path_JAM + '/result_JAM.csv', index=False)
    else:
        df_spikes = pd.read_csv("./output/_spikes.csv", delimiter=" ")
        df_spikes = df_spikes.drop(['population'], axis = 1)
        if not os.path.exists(folder_path_normal):
            os.makedirs(folder_path_normal)
            df_spikes.to_csv(folder_path_normal+"/normal.csv")
        else:
            df_spikes.to_csv(folder_path_normal+"/normal.csv")

