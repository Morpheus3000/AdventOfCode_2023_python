import numpy as np
import cv2


class arr_vis_cv:
    def __init__(self, arr_size=(5, 5),
                 # full_res=(640, 640),
                 full_res=640,
                 pix_size=(10, 10),
                 debug=False):

        self.debug = debug
        # Tested only with squaree

        self.width = full_res
        self.height = full_res

        self.num_rows = arr_size[0]
        self.num_cols = arr_size[1]

        self.pix_width = self.width // self.num_cols
        self.pix_height = self.height // self.num_rows

        self.debug_print('Width -> %d' % self.width)
        self.debug_print('Height -> %d' % self.height)
        self.debug_print('Pix width -> %d' % self.pix_width)
        self.debug_print('Pix height -> %d' % self.pix_height)

        self.num_elements = self.num_rows * self.num_cols

        # self.border_col = np.ones((1, 1, 3))
        self.border_col = np.ones((1, 1))

        self.mem = np.zeros((self.width, self.height, 3))

        self.debug_print('[%s]' % ('-' * 50))
        self.debug_print('\tNum rows: %d, Num cols: %d' % (self.num_rows,
                                                         self.num_cols))
        self.debug_print('\tNum elements: %d' % self.num_elements)
        self.debug_print('[%s]' % ('-' * 50))

    def _sym_2_pix(self, sym):
        ret_pic = np.zeros((self.pix_height, self.pix_width))


        if sym == '/':
            np.fill_diagonal(np.flipud(ret_pic), 1)
        elif sym == '\\':
            np.fill_diagonal(ret_pic, 1)
        elif sym == '|':
            ret_pic[:, self.pix_width // 2] = 1
        elif sym == '-':
            ret_pic[self.pix_height // 2, :] = 1

        # Fill in the borders
        ret_pic[:, 0] = self.border_col
        ret_pic[0, :] = self.border_col

        ret_pic[:, -1] = self.border_col
        ret_pic[-1, :] = self.border_col

        return ret_pic

    def add_arrow(self, pix, dir_dict, tgt_c=1):
        dir_inp = dir_dict['in']
        dir_out = dir_dict['out']
        h, w, _ = pix.shape
        mid_row = h // 2
        mid_col = w // 2

        if dir_inp == 'l':
            pix[mid_row, :mid_col, dir_dict['in_c']] = 1
            pix[mid_row - 1, :mid_col, dir_dict['in_c']] = 1
            pix[mid_row + 1, :mid_col, dir_dict['in_c']] = 1
        elif dir_inp == 'r':
            pix[mid_row, mid_col:, dir_dict['in_c']] = 1
            pix[mid_row - 1, mid_col:, dir_dict['in_c']] = 1
            pix[mid_row + 1, mid_col:, dir_dict['in_c']] = 1
        elif dir_inp == 't':
            pix[:mid_row, mid_col, dir_dict['in_c']] = 1
            pix[:mid_row, mid_col - 1, dir_dict['in_c']] = 1
            pix[:mid_row, mid_col + 1, dir_dict['in_c']] = 1
        elif dir_inp == 'b':
            pix[mid_row:, mid_col, dir_dict['in_c']] = 1
            pix[mid_row:, mid_col - 1, dir_dict['in_c']] = 1
            pix[mid_row:, mid_col + 1, dir_dict['in_c']] = 1

        if dir_out == 'l':
            pix[mid_row, :mid_col, dir_dict['out_c']] = 1
            pix[mid_row - 1, :mid_col, dir_dict['out_c']] = 1
            pix[mid_row + 1, :mid_col, dir_dict['out_c']] = 1
        elif dir_out == 'r':
            pix[mid_row, mid_col:, dir_dict['out_c']] = 1
            pix[mid_row - 1, mid_col:, dir_dict['out_c']] = 1
            pix[mid_row + 1, mid_col:, dir_dict['out_c']] = 1
        elif dir_out == 't':
            pix[:mid_row, mid_col, dir_dict['out_c']] = 1
            pix[:mid_row, mid_col - 1, dir_dict['out_c']] = 1
            pix[:mid_row, mid_col + 1, dir_dict['out_c']] = 1
        elif dir_out == 'b':
            pix[mid_row:, mid_col, dir_dict['out_c']] = 1
            pix[mid_row:, mid_col - 1, dir_dict['out_c']] = 1
            pix[mid_row:, mid_col + 1, dir_dict['out_c']] = 1


    def make_array_vis(self,
                       tgt_data,
                       empty_char):
        lin_data = tgt_data.reshape(self.num_elements)
        for i in range(self.num_elements):
            sym = lin_data[i]
            if sym == empty_char:
                pass
            else:
                pix_sym = self._sym_2_pix(sym)
                pix = self.get_pix_ele(i)
                pix[...] = pix_sym[..., None]

        # init block
        pix = self.get_pix_ele(0)
        self.add_arrow(pix,
                       dir_dict={
                           'in': 'l',
                           'out': 'r',
                           'in_c': 1,
                           'out_c': 0,
                        })

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

        # self.debug_print('[%s]' % ('*' * 50))
        # self.debug_print('\tElement: %d' % ele)
        # self.debug_print('\tArr r: %f, Arr c: %f' % (arr_r, arr_c))
        # self.debug_print('\tPix r: %f, Pix c: %f' % (pix_r, pix_c))
        # self.debug_print('[%s]' % ('*' * 50))

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
            pix[:, 0, :] = self.border_col[..., None]
            pix[0, :, :] = self.border_col[..., None]

            pix[:, -1, :] = self.border_col[..., None]
            pix[-1, :, :] = self.border_col[..., None]


def load_data(data_path):
    lines = [x.strip() for x in open(data_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    grid = np.array([list(x) for x in lines])
    return grid

def tester(file_path):
    data = load_data(file_path)
    print(data)
    print(data.shape)
    img_visser = arr_vis_cv(arr_size=data.shape,
                            # full_res=2200,
                            debug=True)
    img_visser.mark_borders()
    img_visser.make_array_vis(data,
                              empty_char='.')
    while 1:
        cv2.imshow('Visual', img_visser.mem)
        # cv2.resizeWindow('Visual', 640, 480)

        k = cv2.waitKey(100)
        if k == 27:
            break
    cv2.destroyAllWindows()


def demo():
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
    # demo()
    tester(file_path='../data/day16_test.str')
    # tester(file_path='../data/day16_input.str')
