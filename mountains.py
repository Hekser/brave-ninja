import arcade
import random
import bisect

class Mountains():

    def __init__(self, screenWidth):
        self.screenWidth = screenWidth

    def midpoint_displacement(self, start, end, roughness, vertical_displacement = None, num_of_iterations = 16):
        if vertical_displacement is None:
            vertical_displacement = (start[1]+end[1])/2

        points = [start, end]
        iteration = 1

        while iteration <= num_of_iterations:
            points_tup = tuple(points)

            for i in range(len(points_tup)-1):
                midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2, [0, 1]))

                midpoint[1] += random.choice([-vertical_displacement, vertical_displacement])
                
                bisect.insort(points, midpoint)
                
            vertical_displacement *= 2 ** (-roughness)
            
            iteration += 1
        return points

    def fix_points(self, points):
        last_y = None
        last_x = None
        new_list = []
        for point in points:
            x = int(point[0])
            y = int(point[1])

            if last_y is None or y != last_y:
                if last_y is None:
                    last_x = x
                    last_y = y

                x1 = last_x
                x2 = x
                y1 = last_y
                y2 = y

                new_list.append((x1, 0))
                new_list.append((x1, y1))
                new_list.append((x2, y2))
                new_list.append((x2, 0))

                last_x = x
                last_y = y

        x1 = last_x
        x2 = self.screenWidth
        y1 = last_y
        y2 = last_y

        new_list.append((x1, 0))
        new_list.append((x1, y1))
        new_list.append((x2, y2))
        new_list.append((x2, 0))

        return new_list

    def create_mountain_range(self, start, end, roughness, vertical_displacement, num_of_iterations, color_start):

        shape_list = arcade.ShapeElementList()

        layer_1 = self.midpoint_displacement(start, end, roughness, vertical_displacement, num_of_iterations)
        layer_1 = self.fix_points(layer_1)

        color_list = [color_start] * len(layer_1)
        lines = arcade.create_rectangles_filled_with_colors(layer_1, color_list)
        shape_list.append(lines)

        return shape_list

    def getMountains(self, sprites):
        layer_4 = self.create_mountain_range([0, 350], [self.screenWidth, 320], 1.1, 250, 8, (158, 98, 204))
        sprites.append(layer_4)

        layer_3 = self.create_mountain_range([0, 270], [self.screenWidth, 190], 1.1, 120, 9, (130, 79, 138))
        sprites.append(layer_3)

        layer_2 = self.create_mountain_range([0, 180], [self.screenWidth, 80], 1.2, 30, 12, (68, 28, 99))
        sprites.append(layer_2)

        layer_1 = self.create_mountain_range([250, 0], [self.screenWidth, 200], 1.4, 20, 12, (49, 7, 82))
        sprites.append(layer_1)

        return sprites
