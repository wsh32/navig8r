from universe.usb.maestro import Maestro
#
m = Maestro()
# while True:
#         # print('testing')
#         m.set_target(0, 2000)
#from universe.usb.tests.basicMotionTest import Controller

#m = Controller(ttyStr='',device=0x0c)

#print("HI")
while True:
    m.set_target(0, 1500)
    m.set_target(1, 1500)
    m.set_target(2, 1500)
    # print("HI")
