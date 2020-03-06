# ENPM 661 PROJECT 2
# Varun Asthana, Jaad Lepak, Anshuman Singh

# =====SECTION 3: ACTIONS AND NODES=====
def Action(move):
    """8-action move set for robot
        T moves up, costs 1
        L moves left, costs 1
        R moves right, costs 1
        B moves down, costs 1
        TL moves up-left, costs sqrt(2)
        TR moves up-right, costs sqrt(2)
        BL moves down-left, costs sqrt(2)
        BR moves down-right, costs sqrt(2)
        Returns new node position and cost value of the action"""
    actions= {'T': [np.array([-1,0]),1.0], 'L': [np.array([0,-1]),1.0],
              'R': [np.array([0,1]),1.0], 'B': [np.array([1,0]),1.0],
              'TL':[np.array([-1,-1]),math.sqrt(2)], 'TR': [np.array([-1,1]),math.sqrt(2)],
              'BL':[np.array([1,-1]),math.sqrt(2)], 'BR': [np.array([1,1]),math.sqrt(2)] }
    return actions[move]


class AllNodes():
    # Initialize class object
    def __init__(self, height, width):
        """Initializes to keep track of all nodes explored"""
        self.h_ = height + 1
        self.w_ = width + 1
        self.allStates=[]
        self.visited= np.zeros([self.h_, self.w_])
        self.ownIDarr= np.ones([self.h_, self.w_], dtype='int64')*(-1)
        self.pIDarr= np.ones([self.h_, self.w_], dtype='int64')*(-1)
        self.cost2come= np.ones([self.h_, self.w_], dtype='f')*(float('inf'))

    # Function to mark the node as visited in the visited array
    def updateVisited(self, cord):
        self.visited[cord[0], cord[1]] = 1
        return

    # Function to get update cost in cost2come array
    def updateCost(self, cord, cost, pid):
        if(self.cost2come[cord[0],cord[1]] > cost):
            self.cost2come[cord[0],cord[1]] = cost
            self.pIDarr[cord[0],cord[1]] = pid
        return

    # Function to add new unique node in the Nodes data set
    def push(self, cord):
    	self.ownIDarr[cord[0],cord[1]] = int(len(self.allStates))
    	# self.pIDarr[cord[0],cord[1]] = pid
        self.allStates.append(cord)

        return

    # Function to get own id
    def getOwnId(self,cord):
        return self.ownIDarr[cord[0], cord[1]]

    # Function to get parent id
    def getParentId(self,cord):
        return self.pIDarr[cord[0], cord[1]]

    # Function to get state of the node i.e. coordinate [h,w[]
    def getStates(self, idx):
        return self.allStates[idx]

    # Function to get the index value of cost2come array having minimum cost value
    def minCostIdx(self):
        try:
            newMin= np.min(self.cost2come[self.cost2come>0])
            index= np.argwhere(self.cost2come==newMin)[0]
            if(newMin == float('inf')):
                status= False
            else:
                status= True
        except:
            newMin = float ('inf')
            index = np.array([-1,-1])
            status= False
        return status, newMin, index
