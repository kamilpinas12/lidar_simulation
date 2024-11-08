from simulation import Simulation, Object, Keyboard
import simulation

'''
there are two ways to get keyboard input, first if you are using windows you can install keyboard library and set 
keyboard_library to true in simulation/config.json but if you are using mac this library doesn't work so you need to download
pynput and set keyboard_libary to false, punput libary also works on windows but is slower than keyboard

'''


        
if __name__ == '__main__':

    object = Object(100, 100, move_noise_std=0.03, rotation_noise_std=0.004, offset=0, size=8)
    sim = Simulation("maps/map.png", num_measurements=360, distance_std=0.1, angle_std=0.02, lidar_range=600, object=object)

    keyboard = Keyboard()

    while not keyboard.is_key_pressed('q'):
         
        if keyboard.is_key_pressed('w'):
            object.move(4)


        if keyboard.is_key_pressed("s"):
            object.move(-4)

        if keyboard.is_key_pressed('a'):
            object.rotate(0.08)

        if keyboard.is_key_pressed('d'):
            object.rotate(-0.08)

        if keyboard.is_key_pressed('g'):
            lst = sim.get_lidar_data()
            simulation.show_lidar_data(lst, overwrite_file=True)
            sim.update_map(lst, object.x, object.y, object.angle)

        if keyboard.is_key_pressed('h'):
            simulation.show_map(sim.map, sim.occupancy_grid_map.map)
        

        sim.update(show_theoretical_position=True)
        print(object.get_real_position())
    sim.end_sim()


