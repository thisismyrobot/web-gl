#!/usr/bin/env python
#
# jimmyHchan@gmail.com
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
# 
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA


from euclid import Point3, Vector3, Matrix4, Quaternion
import math

class MovableObject3():
    '''A movable, rotatable 3D object with local axes. ''' 
#    some ideas borrowed from Ogre3D's Vector3 and Node class

#    some class constants
    ZERO = Vector3(0, 0, 0)
    UNIT_X = Vector3(1, 0, 0)
    UNIT_Y = Vector3(0, 1, 0)
    UNIT_Z = Vector3(0, 0, 1)
    UNIT_SCALE = Vector3(1, 1, 1)
    DEFAULT_UP = UNIT_Y

    def __init__(self, x, y, z):
        '''Return MovableObject3 object at position x y z with default orientation'''
        self.position = Point3(x, y, z)
        self.local_1_vector = self.UNIT_X
        self.local_1_position = self.position + self.local_1_vector
        self.up_vector = self.DEFAULT_UP
        self.up_position = self.position + self.up_vector

        # get orientation
        self.new_look_at(self.position, self.local_1_position, self.up_position)
       
    def __repr__(self):
        return 'MovableObject(position %s, local_1 %s, up %s)' % \
        (str(self.position),str(self.local_1_position),str(self.up_position))

    def update_coordinates(self):
        '''Hook for subclasses to update the coordinates as the object moves.'''
        raise NotImplementedError 
    
    def new_look_at(self, position, local_1_position, up_position):
        '''Rotate orientation to new positition ala glulookat.'''
#        define u1 as local 1; define u3 based on u1 and up; 
#        find u2 based on u3 and u1
        u1 = local_1_position - position
        up = up_position - position
        u1.normalize()
        up.normalize()
        u3 = u1.cross(up)
        u3.normalize()
        u2 = u3.cross(u1)
        u2.normalize()

        orientation = Matrix4()
#        orientation.identity()
        orientation.a, orientation.e, orientation.i = u1.x, u1.y, u1.z
        orientation.b, orientation.f, orientation.j = u2.x, u2.y, u2.z
        orientation.c, orientation.g, orientation.k = u3.x, u3.y, u3.z
        orientation.d, orientation.h, orientation.l = position.x, position.y, position.z
        self.position = position
        self.orientation = orientation
        self.local_1_position = local_1_position
        self.local_1_vector = u1
        self.up_position = up_position
        self.up_vector = u2
        self.update_coordinates()

    def move_position_by(self, position_delta):
        '''Move object by a distance delta.'''
        assert isinstance(position_delta, Vector3)
        trans_matrix = Matrix4()
#        trans_matrix.identity()
        trans_matrix.d, trans_matrix.h, trans_matrix.l = position_delta.x, position_delta.y, position_delta.z
        self.orientation = trans_matrix * self.orientation
        self.position = trans_matrix * self.position
        self.local_1_position = trans_matrix * self.local_1_position
        self.up_position = trans_matrix * self.up_position
#        update Coordinates 
        self.update_coordinates()

    def move_position_to(self, new_position):
        '''Move object to new position.'''
        assert isinstance(new_position,Vector3) # point3 are vectors3
        position_delta = new_position - self.position
        self.move_position_by(position_delta)

    def rotate_by_angle_axis(self, angle, axis, angle_in_degrees=True, origin=None):
        '''Rotate object by angle about axis. if origin is provided the object is moved, rotated then moved back'''

        assert isinstance(axis, Vector3) 

        if origin:
            assert isinstance(origin, Vector3)
#            move to origin
            self.move_position_by(-origin)

#        convert to radians
        if angle_in_degrees is True:
            angle *= math.pi/180.0

        rot_matrix = Matrix4()
        rot_matrix = rot_matrix.new_rotate_axis(angle, axis)
        self.orientation = rot_matrix * self.orientation
        self.position = rot_matrix * self.position
        self.local_1_position = rot_matrix * self.local_1_position
        self.local_1_vector = self.local_1_position - self.position
        self.up_position = rot_matrix * self.up_position
        self.up_vector = rot_matrix * self.up_vector
#        update Coordinates (not implemented) 
        self.update_coordinates()

        if origin:
#            move back
            self.move_position_by(origin)

    def rotate_to_angle_axis(self, angle, axis, angle_in_degrees=True, origin=None):
        '''Rotate object to angle about axis.'''
#        reset object local_1 and up to the default
        self.local_1_vector = self.UNIT_X
        self.local_1_position = self.position + self.local_1_vector
        self.up_vector = self.DEFAULT_UP
        self.up_position = self.position + self.up_vector
        self.new_look_at(self.position, self.local_1_position, self.up_position)

#        rotate to angle axis
        self.rotate_by_angle_axis(angle, axis, angle_in_degrees, origin)


    def new_orientation(self, orientation):
        '''Define a new orientation for the object.'''
        assert isinstance(orientation, Matrix4)
        self.orientation = orientation
        self.position = self.orientation * self.ZERO
        self.local_1_position = self.orientation * self.local_1_position
        self.local_1_vector = self.local_1_position - self.position
        self.up_position = self.orientation * self.up_position
        self.up_vector = self.up_position - self.position
        self.update_coordinates()
 

class Node3(MovableObject3):
    '''A rotatable movable 3D node with local axes.'''
#    Node3 extends MovableObject3 with a coordinates attribute defined
    def __init__(self, x, y, z):
        MovableObject3.__init__(self, x, y, z)
        self.coordinates = self.position

    def __repr__(self):
        return 'Node3(coordinates %s, local_1 %s, up %s)' % (str(self.position), str(self.local_1_position), str(self.up_position))
    
    def update_coordinates(self):
        self.coordinates = self.position


#class Rectangle3(MovableObject3):
#    '''A rotatable, movable rectangle in 3space.
#    def __init__(self, x, y, z, len_dir_1, len_dir_2, nElements_1, nElements_2):
#        MovableObject3.__init__(self, x, y, z)
#        self.len_dir_1 = len_dir_1
#        self.len_dir_2 = len_dir_2
#        self.nElements_1 = nElements_1
#        self.nElements_2 = nElements_2
#        self.coordinates = self.mesh_grid()

#    def update_coordinates(self):
#        self.mesh_grid()

#    def mesh_grid():
#        pass
        
    
if __name__=='__main__':
    print "new node at 1,2,3"
    n1=Node3(1,2,3)
    print n1

    print "move node by 20,20,-3"
    n1.move_position_by(Vector3(20,20,-3))
    print n1
    
    print "move node to 2,2,3"
    n1.move_position_to(Point3(2,2,3))
    print n1
    
    print "rotate by angle 30deg about z axis 0,0,1 origin at zero"
    n1.rotate_by_angle_axis(30, Vector3(0, 0, 1), angle_in_degrees=True)
    print n1

    print "rotate by angle 30deg about 1,1,1 origin at point"
    n1.rotate_by_angle_axis(30, Vector3(1, 1, 1), angle_in_degrees=True, origin=n1.position)
    print n1
#    coordinate 0.73, 2.72, 3.00
#    local 1 1.40, 3.48, 2.96
#    up 0.07, 3.35, 3.41

    print "rotate by angle 1.2 radians about 1,4,2 axis origin at node"
    n1.rotate_by_angle_axis(1.2, Vector3(1,4,2), angle_in_degrees=False, origin=n1.position)
    print n1
#    coordinate 0.73, 2.72, 3.00
#    local 1 0.74, 3.71, 2.81
#    up 0.65, 2.92, 3.98
