import os
import h5py
import glob as glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


GENUINE_FLAG = 0
IMPOSTOR_FLAG = 1

experiment_result_path = '/home/mlorenzo/WORKSPACE/bob.gradiant.pad.evaluator.mtcnn/results/mtcnn/rgb/mean/ACE/msu-mfsd/pipelines/mtcnn/experiment_result/grandtest/Test'
results = glob.glob(experiment_result_path + '/*.h5')

for i, result in enumerate(results):
    f = h5py.File(result, 'r')
    scores = f.get('scores')[...]
    labels = f.get('labels')[...]
    assert len(scores) == len(labels)
    genuines = scores[labels == GENUINE_FLAG]
    impostors = scores[labels == IMPOSTOR_FLAG]


    plt.figure(i)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    filename, file_extension = os.path.splitext(os.path.basename(result))
    aux = f.get('pipeline_description')[...]
    plt.title(f.get('name_dataset')[()] + ' | ' + 'RBF SVC' + ' | ' + filename)
    n_gen, bins_gen, patches_gen = plt.hist(genuines, bins='auto', facecolor='g', alpha=0.75)
    n_imp, bins_im, patches_im = plt.hist(impostors, bins='auto', facecolor='r', alpha=0.75)
    red_patch = mpatches.Patch(color='red', label='Impostors')
    green_patch = mpatches.Patch(color='green', label='Genuines')

    plt.legend(handles=[red_patch, green_patch])
plt.show()

