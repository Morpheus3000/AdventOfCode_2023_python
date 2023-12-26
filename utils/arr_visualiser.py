import numpy as np
import cv2


class arr_vis_cv:
    def __init__(self, arr_size=(5, 5),
                 # full_res=(640, 640),
                 full_res=640,
                 pix_size=(10, 10),
                 debug=False):

        # Tested only with squaree

        self.width = full_res
        self.height = full_res

        self.num_rows = arr_size[0]
        self.num_cols = arr_size[1]

        self.pix_width = self.width // self.num_cols
        self.pix_height = self.height // self.num_rows

        self.num_elements = self.num_rows * self.num_cols

        self.border_col = np.ones((1, 1, 3))

        self.mem = np.zeros((self.width, self.height, 3))

        self.debug = debug

        self.debug_print('[%s]' % ('-' * 50))
        self.debug_print('\tNum rows: %d, Num cols: %d' % (self.num_rows,
                                                         self.num_cols))
        self.debug_print('\tNum elements: %d' % self.num_elements)
        self.debug_print('[%s]' % ('-' * 50))

    def debug_print(self, debug_strs):
        if self.debug:
            print(debug_strs)

    def arr_2_pix_coords(self, arr_r, arr_c):
        pix_r = arr_r * self.pix_height
        pix_c = arr_c * self.pix_width

        return pix_r, pix_c

    def ele_2_arr(self, ele):
        arr_r = ele // self.num_rows
        arr_c = (ele % self.num_cols)

        return arr_r, arr_c

    def ele_2_pix(self, ele):
        arr_r, arr_c = self.ele_2_arr(ele)
        pix_r, pix_c = self.arr_2_pix_coords(arr_r, arr_c)

        self.debug_print('[%s]' % ('*' * 50))
        self.debug_print('\tElement: %d' % ele)
        self.debug_print('\tArr r: %f, Arr c: %f' % (arr_r, arr_c))
        self.debug_print('\tPix r: %f, Pix c: %f' % (pix_r, pix_c))
        self.debug_print('[%s]' % ('*' * 50))

        return pix_r, pix_c

    def get_pix_ele(self, ele):
        pix_r, pix_c = self.ele_2_pix(ele)
        pix_end_r = pix_r + self.pix_height
        pix_end_c = pix_c + self.pix_width
        pix = self.mem[pix_r:pix_end_r,
                       pix_c:pix_end_c, :]
        return pix

    def update_pix_ele(self, new_pix, ele):
        pix_r, pix_c = ele_2_pix(ele)
        pix_end_r = pix_r + self.pix_height
        pix_end_c = pix_c + self.pix_width
        self.mem[pix_r:pix_end_r,
                 pix_c:pix_end_c, :] = new_pix[:, :, :]

    def mark_borders(self):
        for i in range(self.num_elements):
            # pix = self.get_pix_ele(i + 1)
            pix = self.get_pix_ele(i)
            pix[:, 0, :] = self.border_col
            pix[0, :, :] = self.border_col

            pix[:, -1, :] = self.border_col
            pix[-1, :, :] = self.border_col


def main():
    # Demo random box filler
    img_visser = arr_vis_cv(arr_size=(5, 5),
                            debug=False)
    img_visser.mark_borders()

    reset_border_col = np.array([[[0, 0, 0]]])

    while 1:
        cv2.imshow('Visual', img_visser.mem)

        rand_chan = np.random.randint(3)
        rand_idx = np.random.randint(5 * 5)
        rand_val = np.random.uniform(0, 1)

        tgt_pix = img_visser.get_pix_ele(rand_idx)

        tgt_pix[:, 0, :] = reset_border_col
        tgt_pix[0, :, :] = reset_border_col
        tgt_pix[:, -1, :] = reset_border_col
        tgt_pix[-1, :, :] = reset_border_col

        tgt_pix[:, :, rand_chan] = rand_val

        k = cv2.waitKey(100)
        if k == 27:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
