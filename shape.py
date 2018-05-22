from __future__ import print_function

from PIL import Image, ImageFilter, ImageDraw

from matplotlib.pyplot import imshow

from PIL import Image, ImageFilter, ImageDraw

import matplotlib.pyplot as plt

import math

import random

def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):
    # https://stackoverflow.com/questions/32504246/draw-ellipse-in-python-pil-with-line-thickness/34926008

    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results. 
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[0]]
        right, bottom = [(value - offset) * antialias for value in bounds[1]]
        draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS 
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)
    return image

def rand_uniform(m, M):

    return random.random()*(M - m) + m


#Given the origin of a circle and a random point on that circle,
# rotate the point on that circle to get an equilateral polygon
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    
    The angle is in radians.
    
    """
    
    ox,oy = origin
    
    px,py = point
    
    qx = ox + (math.cos(1 * angle) * (px-ox) - math.sin(1*angle)*(py-oy))
    qy = oy + (math.sin(1 * angle) * (px-ox) + math.cos(1*angle)*(py-oy))
    
    new_point = (qx , qy)
    
    return new_point
    

class TileHandler:
    
    def __init__(self, n_shapes = 1, size = 300, line_k_range = None, circle = None, dot = None, curve = None, polygon_k_range = None, ellipses = None, equilateral_polygon_range = None):
         # if shape parameter is None, then do not draw that shape
            self.n_shapes = n_shapes
            
            self.size = size

            self.line_k_range = line_k_range

            self.polygon_k_range = polygon_k_range

            self.ellipses = ellipses
            
            self.circle = circle
            
            self.dot = dot
            
            self.curve = curve

            self.equilateral_polygon_range = equilateral_polygon_range
            
            self.valid_shapes = []
            
            if line_k_range:
                self.valid_shapes.append("line")
            
            if circle:
                self.valid_shapes.append('circle')
             
            if curve:
                self.valid_shapes.append("curve")
                
            if dot:
                self.valid_shapes.append("dot")
                
            if polygon_k_range:
                self.valid_shapes.append("polygon")

            if ellipses:
                self.valid_shapes.append("ellipses")

            if equilateral_polygon_range:
                self.valid_shapes.append("equilateral_polygon")
             
    def preprocess_tile(self, tile):
        dim = tile['img'].size[0]
        pix = np.array(tile['img'])/255.
        img_vec = pix.reshape(dim, dim, 1)
        description_vec = np.array([tile['description'][key] for key in sorted(tile['description'])])
        return img_vec, description_vec


    def generate_tile(self):

            # https://pillow.readthedocs.io/en/3.1.x/reference/ImageDraw.html

            # http://cglab.ca/~sander/misc/ConvexGeneration/convex.html

            # size: side length of images


            n_shapes = self.n_shapes

            size = self.size

            line_k_range = self.line_k_range
            
            ellipses = self.ellipses

            polygon_k_range = self.polygon_k_range

            equilateral_polygon_range = self.equilateral_polygon_range
            
            dot = self.dot
            
            curve = self.curve
            
            circle = self.circle


            description = dict()


            if self.line_k_range:
                for k in range(line_k_range[0], line_k_range[1]+1):

                    description['line_{}'.format(k)] = 0


            if self.polygon_k_range:
                for k in range(polygon_k_range[0], polygon_k_range[1]+1):

                    description['polygon_filled_{}'.format(k)] = 0

                for k in range(polygon_k_range[0], polygon_k_range[1]+1):

                    description['polygon_unfilled_{}'.format(k)] = 0
                    
           
            if self.dot:
                description['dot'] = 0
                
            if self.curve:
                description['curve'] = 0
                
            if self.circle:
                description['circle_filled'] = 0
                
                description['circle_unfilled'] = 0

            if self.ellipses:
                    description['ellipses_filled'] = 0

                    description['ellipses_unfilled'] = 0

            if self.equilateral_polygon_range:
                for k in range(equilateral_polygon_range[0], equilateral_polygon_range[1]+1):

                    description['equilateral_polygon_filled_{}'.format(k)] = 0

                for k in range(equilateral_polygon_range[0], equilateral_polygon_range[1]+1):

                    description['equilateral_polygon_unfilled_{}'.format(k)] = 0

            img_size = (size, size)

            img = Image.new('L', (img_size), "white")

            img_draw = ImageDraw.Draw(img, 'L')

            for i_shape in range(n_shapes):

                shape_type = random.choice(self.valid_shapes) #random.choice(["line", "dot", "polygon", "ellipse", "equilateral_polygon"])


                if (shape_type == "line") :

                    k = random.randint(line_k_range[0], line_k_range[1]) 
                    # number of pieces the line is made of
                    # generate normalized list of coords
                    # TODO: objects are usually localized, instead of having uniform mass distribution
                    coords = [(random.random(), random.random()) for _ in range(k+1)]

                    # convert coords to pixels
                    coords = [(int(x*size), int(y*size)) for x, y in coords]

                    img_draw.line(coords, width=5)

                    description['line_'+str(k)] += 1

                elif (shape_type == "polygon"):

                    k = random.randint(polygon_k_range[0], polygon_k_range[1]) # number of polygon sides

                    coords = [(rand_uniform(0.25,0.75), rand_uniform(0.25,0.75)) for _ in range(k)]

                    # convert coords to pixels
                    coords = [(int(x*size), int(y*size)) for x, y in coords]

                    filled = random.random() > 0.5
                    if filled:
                        img_draw.polygon(coords, fill="black", outline="black")

                        description['polygon_filled_'+str(k)] += 1
                    else:
                        coords.append(coords[0])
                        img_draw.line(coords, width=5)

                        description['polygon_unfilled_'+str(k)] += 1



                elif (shape_type == 'dot'):
                    
                    top_left_loc = random.random()
                    top_left = (top_left_loc, top_left_loc) #set same top and left location
                    bot_right_loc = rand_uniform(top_left_loc + 0.03, top_left_loc + 0.05)
                    bot_right = (bot_right_loc, bot_right_loc)

                    coords = [top_left, bot_right]

                    # convert coords to pixels
                    coords = [(int(x*size), int(y*size)) for x, y in coords]
                    
                    img_draw.ellipse(coords, fill="black", outline="black")


                    description['dot'] += 1


                elif (shape_type == 'curve'):
                    x_small = rand_uniform(0.2,0.5)
                    y_small = rand_uniform(0.2,0.5)
                    
                    x_large = rand_uniform(0.5 , 0.75)
                    y_large = rand_uniform(0.5 , 0.75)
                    
                    coords = [(x_small, y_small) , (x_large, y_large)]
                    start_angle = rand_uniform(0,180)
                    end_angle = rand_uniform(180,360)
                    
                    # convert coords to pixels
                    coords = [(int(x*size), int(y*size)) for x, y in coords]
                    
                    img_draw.arc(coords, start_angle, end_angle, fill = None)

                    description['curve'] += 1


                elif ( shape_type == "ellipses" ) :

                    # TODO: make these better... right now expected mass dist'n is non-uniform
                    #c = (random.random(), random.random())
                    top_left = (rand_uniform(0.15,0.5), rand_uniform(0.15,0.5))
                    bot_right = rand_uniform(top_left[0], 0.8), rand_uniform(top_left[1], 0.8) 

                    coords = [top_left, bot_right]

                    # convert coords to pixels
                    coords = [(int(x*size), int(y*size)) for x, y in coords]

                    filled = random.random() > 0.5
                    if filled:
                        img_draw.ellipse(coords, fill="black", outline="black")

                        description['ellipses_filled'] += 1

                    else:
                        img = draw_ellipse(img, coords, width=5, outline='black', antialias=4)

                        description['ellipses_unfilled'] += 1
                        
                elif shape_type == "circle":
                    

                    top_left_loc = rand_uniform(0.2,0.5)
                    top_left = (top_left_loc, top_left_loc) #set same top and left location
                    bot_right_loc = rand_uniform(top_left_loc, 0.8)
                    bot_right = (bot_right_loc, bot_right_loc)

                    coords = [top_left, bot_right]

                    # convert coords to pixels
                    coords = [(int(x*size), int(y*size)) for x, y in coords]

                    filled = random.random() > 0.5
                    if filled:
                        img_draw.ellipse(coords, fill="black", outline="black")

                        description['circle_filled'] += 1

                    else:
                        img = draw_ellipse(img, coords, width = 2.5, outline='black', antialias=4)

                        description['circle_unfilled'] += 1

                    
                elif ( shape_type == 'equilateral_polygon' ):

                    origin = (rand_uniform(0.25,0.75), rand_uniform(0.25,0.75))

                    # Todo: given the origin, make a circle within the image region
                    radius_range = [origin[0], origin[1], (1-origin[0]), (1-origin[1])]
                    radius_range.sort()

                    radius = rand_uniform(0.15,radius_range[0])

                    point = (origin[0], (origin[1] + radius))

                    # Choose a random point on the circle and start rotating

                    random_angle = rand_uniform(0, 2*math.pi)

                    starting_point = rotate(origin, point, random_angle)



                    k = random.randint(equilateral_polygon_range[0], equilateral_polygon_range[1]) # number of equilateral polygon sides

                    new = rotate(origin, starting_point, angle = 2*math.pi/k)

                    coords = [starting_point] * k

                    counter = 1

                    #Store starting_points and all rotating points into the coords

                    while (counter <= (k - 1) ):

                        coords[counter] = new

                        new = rotate(origin, new, angle = 2*math.pi/k )

                        counter += 1

                    # convert coords to pixels
                    coords = [(int(x*size), int(y*size)) for x, y in coords]

                    filled = random.random() > 0.5
                    if filled:
                        img_draw.polygon(coords, fill="black", outline="black")

                        description['equilateral_polygon_filled_'+str(k)] += 1
                    else:
                        coords.append(coords[0])
                        img_draw.line(coords, width=5)

                        description['equilateral_polygon_unfilled_'+str(k)] += 1

            del img_draw

            return {"img": img, "description": description}


TH = TileHandler(n_shapes = 1, size = 300, dot = True, circle = None)
tile = TH.generate_tile()

tile_x, tile_y = TH.preprocess_tile(tile)

print("description:", tile['description'])
print("   -> vec:", tile_y)
tile['img'].save('test.png')

def view_image(img):
    imshow(np.asarray(tile['img']))
    

view_image(TH.generate_tile()['img'])
