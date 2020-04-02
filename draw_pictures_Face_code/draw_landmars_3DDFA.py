import numpy as np
import matplotlib.pyplot as plt
import cv2
import scipy.io as sio


image_path = "sample_datas/image00050.jpg"
name = image_path.split(".")[0]
mat_path = name + ".mat"
wfp = name + "_test.jpg"
img_ori = cv2.imread(image_path)
img_mat = sio.loadmat(mat_path)
point_3d68 = img_mat["pt3d_68"]  # 68个特征点
print(point_3d68.shape)


def draw_landmars(img, pts, style='fancy', wfp=None, show_flg=False, **kwargs):
    """Draw landmarks using matplotlib"""
    height, width = img.shape[:2]
    plt.figure(figsize=(12, height / width * 12))
    plt.imshow(img[:, :, ::-1])
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.axis('off')

    if not type(pts) in [tuple, list]:
        pts = [pts]
    for i in range(len(pts)):
        if style == 'simple':
            plt.plot(pts[i][0, :], pts[i][1, :], 'o', markersize=3, color='r')  # g r

        elif style == 'fancy':
            alpha = 0.8
            markersize = 4
            lw = 1.5
            color = kwargs.get('color', 'w')  # w:白色； r
            markeredgecolor = kwargs.get('markeredgecolor', 'black')

            nums = [0, 17, 22, 27, 31, 36, 42, 48, 60, 68]

            # close eyes and mouths
            plot_close = lambda i1, i2: plt.plot([pts[i][0, i1], pts[i][0, i2]], [pts[i][1, i1], pts[i][1, i2]],
                                                 color=color, lw=lw, alpha=alpha - 0.1)
            plot_close(41, 36)
            plot_close(47, 42)
            plot_close(59, 48)
            plot_close(67, 60)

            for ind in range(len(nums) - 1):
                l, r = nums[ind], nums[ind + 1]
                plt.plot(pts[i][0, l:r], pts[i][1, l:r], color=color, lw=lw, alpha=alpha - 0.1)

                plt.plot(pts[i][0, l:r], pts[i][1, l:r], marker='o', linestyle='None', markersize=markersize,
                         color=color,
                         markeredgecolor=markeredgecolor, alpha=alpha)
    if wfp is not None:
        plt.savefig(wfp, dpi=200)
        print('Save visualization result to {}'.format(wfp))
    if show_flg:
        plt.show()


point_3d68s = [point_3d68]
draw_landmars(img_ori, point_3d68s, wfp=wfp, style="fancy", show_flg=True)