

pose =['waiting','aiming']
def control():
    state = pose[0]
    if state == 'waiting':
        angles = [-90,170,0,0]
    if state == 'aiming':
        #solve 
        # h/cos(a0)=l1*cos(a1)+l2*sin(-a2+a1-pi/2),
        # l1*sin(a1)=x+l2*cos(-a2+a1-pi/2),
        # a3=a1-a2-pi/2,a0=pi/6
        #  for a1,a2,a3
        a1 = 0
        a2 = 0
        pass
