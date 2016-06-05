from __future__ import division, print_function

from weirdfitfunction import weirdfit, weirdfunc

from solve_algorithms import solve_svd, solve_QR, solve_normal

import numpy as np

import matplotlib.pyplot as plt

def prediction(data, test = []):
    t, l = data.shape
    clrs = ['red', 'blue', 'green', 'yellow', 'cyan', 'black'] 
    
    x = np.linspace(1, l, l)
    x_pre = np.linspace(l+1, l+6, 6)
    
    
    fig = plt.figure()
    for i in xrange(t):
        plt.plot(x, data[i], marker = 'o', label = 'item '+str(i),
                 color= clrs[i])
    plt.ylim(np.min(data)*0.9, np.max(data)*1.1)
    plt.xlim(0,l+7)
    plt.legend(loc= 'upper left', fontsize = 12)
    plt.savefig('fig1.eps')
    err = []
    for i in xrange(t):
        coeff_svd = weirdfit(x, data[i], dy = np.ones(l), method = 'svd')
        coeff_QR = weirdfit(x, data[i], dy = np.ones(l), method = 'QR')
        coeff_normal = weirdfit(x, data[i], dy = np.ones(l), method = 'normal')

        yfitted_svd = [weirdfunc(x0, coeff_svd) for x0 in x_pre]
        yfitted_QR = [weirdfunc(x0, coeff_QR) for x0 in x_pre]
        yfitted_normal = [weirdfunc(x0, coeff_normal) for x0 in x_pre]
        plt.plot(x_pre, yfitted_svd, color= clrs[i], marker= 's', ls= '')

        if test != []:
            err.append(np.linalg.norm(yfitted_svd-test[i]))
        
    plt.ylim(np.min(data)*0.9, np.max(data)*1.1)
    plt.xlim(0,l+7)
    plt.savefig('fig2.eps')

    #About relative errors
    ys = [yfitted_svd, yfitted_QR, yfitted_normal]
    print('Total relative error between predictions generated by different computational methods')
    print('SVD : SVD Decomposition')
    print('QR : QR decomposition')
    print('NormE: Normal Equations')
    print('\t SVD\t QR\t NormE')
    for y1 in ys:
        if y1 == yfitted_svd:
            print('SVD\t', end = '')
        if y1 == yfitted_QR:
            print('QR\t', end = '')
        if y1 == yfitted_normal:
            print('NormE\t', end = '')
        for y2 in ys:
            y1 = np.array(y1)
            y2 = np.array(y2)
            print(np.linalg.norm(y2-y1)/np.linalg.norm(y1), end = '\t')
        print()

    if test != []:
        print()
        print('Errors (Euclidian norms)')
        for i in xrange(t):
            print('Item ' + str(i) + ': ' + str(err[i]))
        print('Total : ' + str(np.sum(err)))
    
        
    
if __name__ == '__main__':

    a = np.load('../data/data_full.npy')
    #prediction(a)
    prediction(a[:,0:18], test = a[:,18::])
    
