import mdl
from display import *
from matrix import *
from draw import *

ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for command in commands:
        print command

        line = command[0];
            
        if line == 'sphere':
            #print 'SPHERE\t' + str(command)
            add_sphere(tmp,
                       float(command[1]), float(command[2]), float(command[3]),
                       float(command[4]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
            
        elif line == 'torus':
            #print 'TORUS\t' + str(command)
            add_torus(tmp,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
            
        elif line == 'box':
            #print 'BOX\t' + str(command)
            add_box(tmp,
                    float(command[1]), float(command[2]), float(command[3]),
                    float(command[4]), float(command[5]), float(command[6]))
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
            
        elif line == 'circle':
            #print 'CIRCLE\t' + str(command)
            add_circle(tmp,
                       float(command[1]), float(command[2]), float(command[3]),
                       float(command[4]), step)

        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(command)
            add_curve(tmp,
                      float(command[1]), float(command[2]),
                      float(command[3]), float(command[4]),
                      float(command[5]), float(command[6]),
                      float(command[7]), float(command[8]),
                      step, line)                      
            
        elif line == 'line':            
            #print 'LINE\t' + str(command)

            add_edge( tmp,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), float(command[6]) )

        elif line == 'scale':
            #print 'SCALE\t' + str(command)
            t = make_scale(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'move':
            #print 'MOVE\t' + str(command)
            t = make_translate(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]


        elif line == 'rotate':
            #print 'ROTATE\t' + str(command)
            theta = float(command[2]) * (math.pi / 180)
            
            if command[1] == 'x':
                t = make_rotX(theta)
            elif command[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
                
        elif line == 'clear':
            tmp = []
            
        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, tmp )

        elif line == 'push':
            stack.append( [x[:] for x in stack[-1]] )
            
        elif line == 'pop':
            stack.pop()

        elif line == 'display' or line == 'save':
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, command[1])
        
