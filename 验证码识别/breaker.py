 #-*- coding: UTF-8 -*-

from PIL import Image, ImageFilter, ImageEnhance

def parser( im ):

    #加亮
    enhance = ImageEnhance.Brightness( im )
    im = enhance.enhance( 1.2 )
    im.save("test/01.png")
    im.show()

    #提高对比度
    enhance = ImageEnhance.Contrast( im )
    im = enhance.enhance( 20 )
    im.save('test/02.png')
    im.show()

    #中值去噪
    im = im.convert('1')
    im = im.filter( ImageFilter.MedianFilter() )
    im.save('test/03.png')
    im.show()
    
    
    
    return im

def main():
    im = Image.open( "test/0.png" )
    im.show()
    
    im = parser( im )
    
    imim = im.load()
    WIDTH = im.size[0]
    HEIGHT = im.size[1]
    
    i = 0
    has_start = False
    chars = []
    start_x = 0
    end_x = 0
    
    while i < WIDTH:
        all_none = True
        for j in xrange(HEIGHT):
            if imim[i, j] != 255:
                all_none = False
        if all_none:
            if has_start:
                end_x = i
                has_start = False
                char = im.crop((start_x, 0, end_x, HEIGHT))
                #char.show()
 
                charchar = char.load()
                width = end_x - start_x
                y1 = 0
                y2 = HEIGHT - 1
                all_none = True
                while all_none:
                    for ii in xrange(width):
                        if charchar[ii, y1] != 255:
                            all_none = False
                            break
                    y1 += 1
                
                all_none = True
                while all_none:
                    for ii in xrange(width):
                        if charchar[ii, y2] != 255:
                            all_none = False
                            break
                    y2 -= 1
                    
                char = char.crop((0, y1 - 1, width, y2 + 2))
                char = char.resize((20, 20))
                #char.show()
 
                chars.append(char)
        else:
            if not has_start:
                start_x = i
                has_start = True
        i += 1
    
    '''
    file = open('test/xinlang.img', 'a')
    for char in chars:
        nstr = ''
        im_loaded = char.load()
        for x in range(20):
            for y in range(20):
                if im_loaded[x, y] == 255:
                    nstr += '0'
                else:
                    nstr += '1'
        char.show()
        n = raw_input( "该图片为：" )
        file.write(nstr+':'+n+'\n')
    file.close()
    '''
        
    pattern = []
    for l in open('test/xinlang.img', 'r').read().split('\n'):
        pattern.append(l.split(':'))
    del pattern[-1]
    
    for char in chars:
        im = char.load()
        nstr = ''
        for x in xrange(20): #生成目标图像的特征字符串
            for y in xrange(20):
                if im[x, y] == 255:
                    nstr += '0'
                else:
                    nstr += '1'
        minmin = 400
        res = None
        for p in pattern:
            cur = 0
            for i in xrange(400):
                if nstr[i] != p[0][i]: #比对每一个像素，如果不相同，则增加差异值
                    cur += 1
            if cur <= minmin: #记录下差异值最小时所对应的字符
                minmin = cur
                res = p[1]
        print res
    
if __name__ == "__main__":
    main()
    print "done"
