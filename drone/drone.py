from swarm import SingleClover

def drone():
    clover = SingleClover("clover0", 0)
    clover.navigateWait(z=1, auto_arm=True)

if __name__ == "__main__":
    drone()