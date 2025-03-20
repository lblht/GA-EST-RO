from scipy.spatial import Delaunay
import utils as utils
import numpy as np
import math

def get_delaunay_steiner_points(terminals):
    if len(terminals) <= 2: return []
    delaunay = Delaunay(terminals)
    delaunay_steiner_points = []

    for simplex in delaunay.simplices:
        triangle = [terminals[simplex[0]], terminals[simplex[1]], terminals[simplex[2]]]
        torricelli_point = get_torricelli_point(triangle)
        delaunay_steiner_points.append(torricelli_point)
    
    return delaunay_steiner_points

def get_torricelli_point(triangle):
    A, B, C = triangle

    angle_A = utils.angle_between_edges(B, A, C)
    angle_B = utils.angle_between_edges(A, B, C)
    angle_C = utils.angle_between_edges(A, C, B)

    if angle_A >= 120:
        return A
    elif angle_B >= 120:
        return B
    elif angle_C >= 120:
        return C

    A2 = third_point_of_equilateral(B, C)
    B2 = third_point_of_equilateral(C, A)
    C2 = third_point_of_equilateral(A, B)

    line1 = (A[0], A[1], A2[0], A2[1])
    line2 = (B[0], B[1], B2[0], B2[1])
    line3 = (C[0], C[1], C2[0], C2[1]) # not used, two lines are enough to find the intersection
    
    intersection = find_intersection(line1, line2)
    return intersection

def rotate_point(px, py, cx, cy, angle):
    s = math.sin(angle)
    c = math.cos(angle)
    px -= cx
    py -= cy
    xnew = px * c - py * s
    ynew = px * s + py * c
    px = xnew + cx
    py = ynew + cy
    return px, py

def third_point_of_equilateral(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    p3 = rotate_point(x2, y2, x1, y1, -math.pi / 3)
    return p3

def find_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    A = np.array([[x2 - x1, -(x4 - x3)],[y2 - y1, -(y4 - y3)]])
    b = np.array([x3 - x1, y3 - y1])
    t, s = np.linalg.solve(A, b)
    intersection_x = x1 + t * (x2 - x1)
    intersection_y = y1 + t * (y2 - y1)
    return intersection_x, intersection_y