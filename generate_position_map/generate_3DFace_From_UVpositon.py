"""
如何 从 Position Map 产生 3D Face
"""
import numpy as np
import os
from skimage.io import imread, imsave

# 类似 超参数
uv_kpt_ind = np.loadtxt("datas/uv-data/uv_kpt_ind.txt").astype(np.int32)  # 2 x 68 get kpt
face_ind = np.loadtxt("datas/uv-data/face_ind.txt").astype(np.int32)  # get valid vertices in the pos map
triangles = np.loadtxt("datas/uv-data/triangles.txt").astype(np.int32)  # ntri x 3


# 测试一个例子
face_url = "datas/image00050.jpg"
face_texture_url = "datas/image00050_tex.jpg"
# Label 是 npy 数据， 可不是  position map图像(只是用来显示看的)
face_posmap_url = "datas/image00050.npy"

global resolution_op
resolution_op = 256
# 设置参数
uv_h = uv_w = 256
image_h = image_w = 256

image_posmap = np.load(face_posmap_url)
print(image_posmap.shape)
print(np.max(image_posmap))


# 从 Position Map 获取 顶点
def get_vertices(pos):
    '''
    Args:
        pos: the 3D position map. shape = (256, 256, 3).
    Returns:
        vertices: the vertices(point cloud). shape = (num of points, 3). n is about 40K here.
    '''
    all_vertices = np.reshape(pos, [resolution_op ** 2, -1])
    vertices = all_vertices[face_ind, :]  # face_ind 是什么呢？

    return vertices


def get_landmarks(pos):
    """
    Args:
        pos: the 3D position map. shape = (256, 256, 3).
    Returns:
        kpt: 68 3D landmarks. shape = (68, 3).
    :param pos:
    :return:
    """
    kpt = pos[uv_kpt_ind[1, :], uv_kpt_ind[0, :], :]
    return kpt


kpt = get_landmarks(image_posmap)
print(kpt.shape)  # (68, 3)  68个关键点

vertices = get_vertices(image_posmap)
print(vertices.shape)  # (43867, 3) PRNet 人脸是 43867 个顶点


# 保存顶点  不保存纹理
def dump_to_ply(vertex, tri, wfp):
    header = """ply
    format ascii 1.0
    element vertex {}
    property float x
    property float y
    property float z
    element face {}
    property list uchar int vertex_indices
    end_header"""
    n_vertex = vertex.shape[1]  # ((3, 43867))
    n_face = tri.shape[1]   # ((3, 86906))
    header = header.format(n_vertex, n_face)

    with open(wfp, 'w') as f:
        f.write(header + '\n')
        for i in range(n_vertex):  # 顶点
            x, y, z = vertex[:, i]
            f.write('{:.4f} {:.4f} {:.4f}\n'.format(x, y, z))
        for i in range(n_face):  # 三角形
            idx1, idx2, idx3 = tri[:, i]
            f.write('3 {} {} {}\n'.format(idx1 - 1, idx2 - 1, idx3 - 1))
    print('Dump tp {}'.format(wfp))


save_prefix = "results/"
name = face_url.split("/")[-1].split(".")[0] + ".ply"
print(name)
face_ply = os.path.join(save_prefix, name)

# 保存 顶点信息 shape 成功
dump_to_ply(vertices.T, triangles.T, face_ply)   # 切记 tri 是 /Data/uv-data/triangles.txt 中的三角


# 保存 带上 color/texture 信息
def get_colors(image, vertices):
    """
        Args:
            pos: the 3D position map. shape = (256, 256, 3).
        Returns:
            colors: the corresponding colors of vertices. shape = (num of points, 3). n is 45128 here.
    """
    [h, w, _] = image.shape
    vertices[:, 0] = np.minimum(np.maximum(vertices[:, 0], 0), w - 1)  # x
    vertices[:, 1] = np.minimum(np.maximum(vertices[:, 1], 0), h - 1)  # y
    ind = np.round(vertices).astype(np.int32)
    colors = image[ind[:, 1], ind[:, 0], :]  # n x 3

    return colors


image_face = imread(face_url)  # face_url 是 剪切后为（256， 256， 3）的人脸图像
[h, w, c] = image_face.shape
print(h, w, c)
image_face = image_face / 255.
colors = get_colors(image_face, vertices)  # 从人脸 和 顶点 中获取 color (43867, 3)
print(colors.shape)


# 写入 .obj文件，具有colors （texture）
def write_obj_with_colors(obj_name, vertices, triangles, colors):
    ''' Save 3D face model with texture represented by colors.
    Args:
        obj_name: str
        vertices: shape = (nver, 3)
        colors: shape = (nver, 3)
        triangles: shape = (ntri, 3)
    '''
    triangles = triangles.copy()
    triangles += 1  # meshlab start with 1

    if obj_name.split('.')[-1] != 'obj':
        obj_name = obj_name + '.obj'

    # write obj
    with open(obj_name, 'w') as f:

        # write vertices & colors
        for i in range(vertices.shape[0]):
            # s = 'v {} {} {} \n'.format(vertices[0,i], vertices[1,i], vertices[2,i])
            s = 'v {} {} {} {} {} {}\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2], colors[i, 0],
                                               colors[i, 1], colors[i, 2])
            f.write(s)

        # write f: ver ind/ uv ind
        [k, ntri] = triangles.shape
        for i in range(triangles.shape[0]):
            # s = 'f {} {} {}\n'.format(triangles[i, 0], triangles[i, 1], triangles[i, 2])
            s = 'f {} {} {}\n'.format(triangles[i, 2], triangles[i, 1], triangles[i, 0])
            f.write(s)
name = face_url.split("/")[-1].split(".")[0] + ".obj"
save_vertices = vertices.copy()
save_vertices[:, 1] = h - 1 - save_vertices[:, 1]  # 这一步 不可缺少； (43867, 3)
write_obj_with_colors(os.path.join(save_prefix, name), save_vertices, triangles, colors)  # save 3d face(can open with meshlab)
