import subprocess
import os
import sys
from pydub import AudioSegment
import numpy as np
'''

try:

    os.system("ffmpeg")
    
except:
    print("Please Install ffmpeg first")
    sys.exit()
'''

def data_mp3(input_file):

    song=AudioSegment.from_mp3(input_file)
    
    length=len(song)

    data=[]

    for i in range(length):

        rsong=song[i]
        count=0
        while True:

            d=rsong.get_frame(count)

            if d==b'':
                
                break
            count=count+1

            d=np.frombuffer(d,'int16')
            data.append(d)

    return np.array(data)
    



def get_info(input_file,chunk_size=1000000):

    command='ffprobe -i '+input_file

    res=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    res=res.stdout.read(chunk_size)
    return res.decode()

def execute(command):

    try:
        subprocess.call(command)

        return True
    except:
        print("Error")
        return False



def cvtImg2Video(imgName,imgExt,output_video):

    command='ffmpeg -f image2 -i '+imgName+'%d.'+imgExt +' '+output_video

    return execute(command)


def cvtVideo2Img(input_video,img_name,img_ext,img_path=''):

    command='ffmpeg -i '+input_video+' '+img_path+img_name+'%d.'+img_ext
    print(command)

    return execute(command)


def cropVideo(input_video,out_w,out_h,x,y,output_video):
    out_w=str(out_w)
    out_h=str(out_h)
    x=str(x)
    y=str(y)
    command='ffmpeg -i '+input_video+' -filter:v "crop='+out_w+':'+out_h+':'+x+':'+y+'" ' +output_video

    return execute(command)


def scaleVideo(input_video,scale,output_video):
    h=scale[0]
    w=scale[1]
    h=str(h)
    w=str(w)

    command='ffmpeg -i '+input_video+' -vf scale='+h+':'+w+' '+output_video

    return execute(command)


def scaleImage(input_img,scale,output_img):

    return scaleVideo(input_img,scale,output_img)


def cut_vid_from_vid(original_file,startT,durationT,output_file):
    command='ffmpeg -ss {0} -i {1} -t {2} -vcodec copy -acodec copy {3}'.format(startT,original_file,durationT,output_file)
    print(command)
    return execute(command)

def extract_sound_from_vid(input_video,output_audio,outExt='mp3',frameRate=44100,bitRate=192,channel=2):
    frameRate=str(frameRate)
    bitRate=str(bitRate)
    command='ffmpeg -i {0} -vn -ar {1} -ac {2} -ab {3}k -f {4} {5}'.format(input_video,frameRate,channel,bitRate,outExt,output_audio)
    print(command)
    return execute(command)

def cvt_audio_format(input_file,output_file,outExt='mp3',frate=44100,channel=2,bitrate=192):
    frate=str(frate)
    channel=str(channel)
    bitrate=str(bitrate)

    command='ffmpeg -i {0} -vn -ar {1} -ac {2} -ab {3}k -f {4} {5}'.format(input_file,frate,channel,bitrate,outExt,output_file)
    print(command)

    return execute(command)

def cvt_video_format(input_file,output_file):
    command='ffmpeg -i {0} {1}'.format(input_file,output_file)
    print(command)
    return execute(command)


def compress_video(input_file,output_file,scale):
    h=scale[0]
    w=scale[1]

    command='ffmpeg -i {0} -s {1}x{2} -vcodec msmpeg4v2 {3}'.format(input_file,h,w,output_file)

    return execute(command)

def create_animated_gif(input_file,output_file):
    command='ffmpeg -i {0} {1}'.format(input_file,output_file)

    return execute(command)

def mix_video_with_sound(input_audio,input_video,output_video):
    command='ffmpeg -i {0} -i {1} {2}'.format(input_audio,input_video,output_video)

    return execute(command)

def add_text_subtitle_2_video(input_video,output_video,text='mov_text',subtitles='subtitles.srt'):

    command='ffmpeg -i {0} -i {1} -c copy -c:s {2} {3}'.format(input_video,subtitles,text,output_video)

    return execute(command)

def overlay_image_on_video(input_video,input_image,output_video,over_pos,durFrom,durTo):
    
    command='ffmpeg -i {0} -i {1} -filter_complex "[0:v][1:v] overlay={2}:{3}:enable='+"'"+'between(t,{4},{5})'+"'"+'" -pix_fmt yuv420p -c:a copy {6}'
   
    command=command.format(input_video,input_image,over_pos[0],over_pos[1],durFrom,durTo,output_video)
             
    print(command)
    return execute(command)
