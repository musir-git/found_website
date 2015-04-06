
import urllib

def main():
    srctitle = "http://s.weibo.com/ajax/pincode/pin?type=sass&ts="
    for i in range(0, 1000 ):
        url = srctitle + str(i)
        mt = urllib.urlopen( url)
        c = mt.read()
        
        fout = open( "pins/" +str(i)+".png", 'wb')
        fout.write( c )
        fout.close()
        
if __name__=="__main__":
    main()
    print "done"