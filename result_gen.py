import easyocr
import cv2
import numpy as np

src_fn = './resource/numerals.png'
x_fn = './resource/x_button.jpg'

def geometry(image,x_button=x_fn,thres=100000,debug=False):
    h = 37
    w = 43
    size = 34
    x = cv2.imread(x_button)
    x_gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    roi = image[h:h+size,w:w+size]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    template = cv2.resize(x_gray,(size,size))
    match = cv2.matchTemplate(roi_gray,template,cv2.TM_CCOEFF)
    if debug:
        cv2.imshow('debug',roi_gray)
        cv2.waitKey(0)
        return match
    else:
        return match > thres

def numerals(src_f=src_fn):
    src_in = cv2.imread(src_f)
    src = cv2.cvtColor(src_in, cv2.COLOR_BGR2GRAY)

    num_w = 51
    num_h = 73
    gap = 1
    nums = []
    idx = 0
    for i in range(12):
        if idx == 3:
            num = np.zeros((num_h,num_w)).astype(np.uint8)
            num[:,17:34] = src[gap+(num_h+gap)*i:gap+(num_h+gap)*i+num_h,gap:gap+17]
        elif idx == 5:
            num = np.zeros((num_h,num_w)).astype(np.uint8)
            num[:,3:48] = src[gap+(num_h+gap)*i:gap+(num_h+gap)*i+num_h,gap:gap+45]
        elif idx == 9:
            num = np.zeros((num_h,num_w)).astype(np.uint8)
            num[:,3:48] = src[gap+(num_h+gap)*i:gap+(num_h+gap)*i+num_h,gap:gap+45]
        else:
            num = src[gap+(num_h+gap)*i:gap+(num_h+gap)*i+num_h,gap:gap+num_w]
        idx +=1
        nums.append(num)

    return nums[2:]

def num_match(score_in,num_size,thres=700000,debug=False):
    if debug:
        nums = numerals()
        maxres = -np.inf
        pred = -1
        for idx,num in enumerate(nums):
            template = cv2.resize(num,num_size)
            scores = [score_in,cv2.bitwise_not(score_in)]
            for score in scores:
                res = cv2.matchTemplate(score,template,cv2.TM_CCOEFF)
                print(idx,pred,res)
                if res > maxres:
                    pred = idx
                    maxres = res
        return pred

    else:
        nums = numerals()
        maxres = thres
        pred = -1
        for idx,num in enumerate(nums):
            template = cv2.resize(num,num_size)
            scores = [score_in,cv2.bitwise_not(score_in)]
            for score in scores:
                res = cv2.matchTemplate(score,template,cv2.TM_CCOEFF)
                if res > maxres:
                    pred = idx
                    maxres = res
        return pred

def num_match_pos(score_in,num_size,thres=700000,debug=False):
    if debug:
        nums = numerals()
        maxres = -np.inf
        pred = -1
        for idx,num in enumerate(nums):
            template = cv2.resize(num,num_size)
            res = cv2.matchTemplate(score_in,template,cv2.TM_CCOEFF)
            print(idx,pred,res)
            if res > maxres:
                pred = idx
                maxres = res
        return pred

    else:
        nums = numerals()
        maxres = thres
        pred = -1
        for idx,num in enumerate(nums):
            template = cv2.resize(num,num_size)
            res = cv2.matchTemplate(score_in,template,cv2.TM_CCOEFF)
            if res > maxres:
                pred = idx
                maxres = res
        return pred

def id_process(ocr,id_img):
    results = ocr.readtext(id_img,slope_ths=5,ycenter_ths=25,height_ths=25,width_ths=25)
    id, prob = '',0.0
    if len(results) == 0:
        pass
    else:
        for r in results:
            _, ri, rp = r
            if rp > prob:
                prob = rp
                id = ri
    return id, prob

def read_image(img_in,type=-1,pos=0,gpu=False):

    types = [0,1]
    if type not in types:
        type = int(geometry(img_in)[0][0])

    if type == 0:
        h_start = 133
        h_d = 34
        h_gap = 8

        #id
        i_start = 145
        i_end = 400

        #score
        s_width = 21
        s_height = 30
        s_end = 586
        s_gap = 2
        
    else:
        h_start = 51
        h_d = 46
        h_gap = 6

        #id
        i_start = 670
        i_end = 925

        #score
        s_width = 17
        s_height = 27
        s_end = 1217
        s_gap = 0
    
    poss = np.arange(12).astype(np.uint8)+1
    try:
        pos = int(pos)
        if pos not in poss:
            pos = 0
    except ValueError:
        pos = 0

    reader_en = easyocr.Reader(['en'], gpu=gpu)
    reader = easyocr.Reader(['ja','en'], gpu=gpu)

    img = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
    h,w = img.shape
    #resize
    if h!=720 or w!=1280:
        img = cv2.resize(img,(1280,720))

    id_out = []
    score_out = []

    if pos == 0:
        for i in range(12):
            id = img[h_start+(h_gap+h_d)*i:h_start+(h_gap+h_d)*i+h_d,i_start:i_end]
            if type == 0:
                score1 = img[h_start+(h_gap+h_d)*i+2:h_start+(h_gap+h_d)*i+h_d-2,s_end-3*s_width-2*s_gap:s_end-2*s_width-2*s_gap]
                score2 = img[h_start+(h_gap+h_d)*i+2:h_start+(h_gap+h_d)*i+h_d-2,s_end-2*s_width-s_gap:s_end-(s_width+s_gap)]
                score3 = img[h_start+(h_gap+h_d)*i+2:h_start+(h_gap+h_d)*i+h_d-2,s_end-s_width:s_end]
            else:
                score1 = img[h_start+(h_gap+h_d)*i+13:h_start+(h_gap+h_d)*i+h_d-6,s_end-3*s_width-2*s_gap-1:s_end-2*s_width-2*s_gap-1]
                score2 = img[h_start+(h_gap+h_d)*i+13:h_start+(h_gap+h_d)*i+h_d-6,s_end-2*s_width-s_gap:s_end-(s_width+s_gap)]
                score3 = img[h_start+(h_gap+h_d)*i+13:h_start+(h_gap+h_d)*i+h_d-6,s_end-s_width:s_end]

            scores = [score1,score2,score3]
            
            score_result=''
            for s in scores:
                pred = num_match(s,num_size=(s_width,s_height),debug=False)
                if pred>-1:
                    score_result+=str(pred)

            id_en, prob_en = id_process(reader_en,id)
            id_jp, prob_jp = id_process(reader,id)

            if prob_en > prob_jp:
                id_result = id_en
            else:
                id_result = id_jp

            id_out.append(id_result)
            score_out.append(score_result)

    else:
        for i in range(12):
            id = img[h_start+(h_gap+h_d)*i:h_start+(h_gap+h_d)*i+h_d,i_start:i_end]
            if type == 0:
                score1 = img[h_start+(h_gap+h_d)*i+2:h_start+(h_gap+h_d)*i+h_d-2,s_end-3*s_width-2*s_gap:s_end-2*s_width-2*s_gap]
                score2 = img[h_start+(h_gap+h_d)*i+2:h_start+(h_gap+h_d)*i+h_d-2,s_end-2*s_width-s_gap:s_end-(s_width+s_gap)]
                score3 = img[h_start+(h_gap+h_d)*i+2:h_start+(h_gap+h_d)*i+h_d-2,s_end-s_width:s_end]
            else:
                score1 = img[h_start+(h_gap+h_d)*i+13:h_start+(h_gap+h_d)*i+h_d-6,s_end-3*s_width-2*s_gap-1:s_end-2*s_width-2*s_gap-1]
                score2 = img[h_start+(h_gap+h_d)*i+13:h_start+(h_gap+h_d)*i+h_d-6,s_end-2*s_width-s_gap:s_end-(s_width+s_gap)]
                score3 = img[h_start+(h_gap+h_d)*i+13:h_start+(h_gap+h_d)*i+h_d-6,s_end-s_width:s_end]

            if i+1 == pos:
                scores = [cv2.bitwise_not(score1),cv2.bitwise_not(score2),cv2.bitwise_not(score3)]
            else:
                scores = [score1,score2,score3]
            
            score_result=''
            for s in scores:
                pred = num_match_pos(s,num_size=(s_width,s_height),debug=False)
                if pred>-1:
                    score_result+=str(pred)

            id_en, prob_en = id_process(reader_en,id)
            id_jp, prob_jp = id_process(reader,id)

            if prob_en > prob_jp:
                id_result = id_en
            else:
                id_result = id_jp
            
            id_out.append(id_result)
            score_out.append(score_result)

    return id_out, score_out

if __name__ == '__main__':
    fn = './tests/FB7dGLhUYAIs49H.jpeg'
    img = cv2.imread(fn)
    id, score = read_image(img, type=1)
    print(id)
    print(score)
