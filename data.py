data_1=[]
data_2=[]
for i in range(2):
    #inputting velocity data for data file i+1
    pos_li=[]
    with open("DATA_"+str(i+1)+"/POS/pos_data.txt","r") as pos:
        poslines=pos.readlines()
        for line in poslines:
            pos_li.append(line.strip(" ").split())
    pos.close()
    #-----------------------------------------------
    #inputting velocity data for data file i+1
    vel_li=[]
    vel=open("DATA_"+str(i+1)+"/VEL/vel_data.txt","r")
    with open("DATA_"+str(i+1)+"/VEL/vel_data.txt","r") as vel:
        vellines=vel.readlines()
        for line in vellines:
            vel_li.append(line.strip(" ").split())
    vel.close()
    #--------------------------------
    #ts is a 3d list
    if i==0:
        data_1.append(pos_li)
        data_1.append(vel_li)
    else:
        data_2.append(pos_li)
        data_2.append(vel_li)


