import os 
import shutil

def text_creator():
    os.chdir('dataset')

    if 'newDataset' not in os.listdir(os.getcwd()):
        os.mkdir('newDataset')

    root = os.getcwd()
    directories = os.listdir(os.getcwd())
    dir_count = 1

    for curr_dir in directories:
        if curr_dir != 'newDataset':
            os.chdir(curr_dir)

            for text in os.listdir(os.getcwd()):
                source = os.getcwd() + '/%s'  % text
                target =  root + '/newDataset'
                shutil.copy(source, target)

                new_source = target + '/%s' % text
                new_name = target + '/0%s.txt' % str(dir_count)

                os.rename(new_source, new_name)

                dir_count += 1

            os.chdir('../')

if __name__ == '__main__':
    text_creator()