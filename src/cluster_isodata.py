import numpy as np

def cluster_isodata(x, ninit_clusters, theta_n, theta_s, theta_c, exp_clusters, combL, max_iters):
    """
    @Intro: Implementation of ISODATA algorithm, an unsupervised cluster algorithm
            ISODATA: Iterative Self Organizing Data Analysis Techniques Algorithm

    @params x: numpy input samples, every line represents a sample
    @params ninit_clusters: initial cluster numbers
    @params theta_n: threshold numbers at least one cluster should have
    @params theta_s: threshold of standard deviation one cluster should have
    @params theta_c: threshold of distance that two clusters merges
    @params exp_clusters: expected cluster numbers
    @params combL: maximum number of combination for each iterations

    """
    
    # used in separate clusters
    split = 0.5

    def find_first_not(src, mask):
        """ return the index and content of the first not occurence of item in src not in mask """
        for i, item in enumerate(src):
            if item not in mask:
                return (i, item)
        return (-1, None)

    nsamples, vec_length = x.shape
    
    centers_idx = np.random.permutation(nsamples)[:ninit_clusters]
    centers = x[centers_idx].astype(float)
    nclusters = ninit_clusters
    
    iterations = 1
    while iterations <= max_iters:

        x_clones = np.tile(x, (nclusters, 1, 1))
        centers_clones = [np.tile(centers[i], (nsamples, 1)) for i in xrange(nclusters)]
        centers_clones = np.asarray(centers_clones, dtype = np.float32)
    
        dist = np.sqrt(np.sum(np.square(x_clones - centers_clones), axis = 2)).transpose()
        x_dist_min = np.min(dist, axis = 1)
        x_class = np.argmin(dist, axis = 1)
    
        # center stores center point vector data
        # c stores which samples are around center i
        # c_rm stores center to be removed
        c = [[] for i in range(nclusters)]
        c_rm = []
        for i in xrange(nsamples):
            c[x_class[i]].append(i)
         
        # remove the center that have numbers smaller than theta_n and re-weighting centers
        for i in xrange(nclusters):
            if len(c[i]) < theta_n:
                # remove this center
                c_rm.append(i)
                for idx in c[i]:
                    nearest_c = np.argsort(dist[idx])
                    flag, c_newidx = find_first_not(list(nearest_c), c_rm)

                    if flag < 0:
                        print 'fatal error occurs here #51'
                
                    c[c_newidx].append(idx)
        c_rm = sorted(c_rm, reverse = True) 
        for del_idx in c_rm:
            centers = np.delete(centers, (del_idx), axis = 0)
            del c[del_idx]
        nclusters -= len(c_rm)

        for i in xrange(nclusters):
            centers[i] = np.sum(x[c[i]], axis = 0, dtype = np.float32) / len(c[i])
        # end of removing and re-weighting

        # calculate average distance for each cluster group
        avg_dist_c = []
        all_dist = 0
        for i in xrange(nclusters):
            cnum = len(c[i])
            cclones = np.tile(centers[i], (cnum, 1))
            csdist = np.sum(np.sqrt(np.sum(np.square(cclones - x[c[i]]), axis = 1), dtype = np.float32))
            all_dist += csdist
            avg_dist_c.append(csdist / cnum)

        all_dist /= nsamples
        if iterations == max_iters:
            theta_c = 0
        elif nclusters <= exp_clusters / 2 or (iterations % 2 == 1 and nclusters < 2 * exp_clusters):
            # make center split
            is_split = False
            max_sigma = []
            argmax_sigma = []
            for i in xrange(nclusters):
                x_tmp = x[c[i]].astype(float)
                center_clones_tmp = np.tile(centers[i], (len(c[i]), 1))
                sigma_i = np.sqrt(np.sum(np.square(x_tmp - center_clones_tmp), axis = 0, dtype = np.float32) / len(c[i]))
                argmax_sigma.append(np.argmax(sigma_i))
                max_sigma.append(np.max(sigma_i))

            for i in range(nclusters):
                if max_sigma[i] > theta_s:
                    if (avg_dist_c[i] > all_dist and len(c[i]) > 2 * theta_n + 2) or nclusters <= exp_clusters / 2:
                        nclusters += 1
                        center_plus = np.copy(centers[i])
                        center_minus = np.copy(centers[i])
                        
                        center_plus[argmax_sigma[i]] += split * max_sigma[i]
                        center_minus[argmax_sigma[i]] -= split * max_sigma[i]

                        centers = np.vstack([centers, center_minus]) 
                        centers[i] = center_plus
                        is_split = True
            if is_split:
                continue
        
        # center-center distance
        ccdist = []
        ccdist_idx = []
        cmerge_idx = set()
        for i in xrange(nclusters):
            for j in xrange(i + 1, nclusters):
                ccdist_ij = np.sqrt(np.sum(np.square(centers[i] - centers[j])))
                if ccdist_ij < theta_c:
                    cmerge_idx.add(i)
                    cmerge_idx.add(j)
                    ccdist.append(ccdist_ij)
                    ccdist_idx.append((i, j))

        ccdist = np.array(ccdist)
        ccdist_sorted_idx = np.argsort(ccdist)
        ccdist_idx = np.array(ccdist_idx)[ccdist_sorted_idx]
        
        # merge centers using theta_c
        this_comb = 0
        for i in xrange(ccdist_idx.shape[0]):
            if this_comb > combL:
                break
            ci = ccdist_idx[i][0]
            cj = ccdist_idx[i][1]
            if ci in cmerge_idx and cj in cmerge_idx:
                centers = np.vstack([centers, (centers[ci] * len(c[ci]) + centers[cj] * len(c[cj])) / (len(c[ci]) + len(c[cj]))])
                c.append(c[cj][:] + c[ci][:])
            
                if ci < cj:
                    ci, cj = cj, ci
                del c[ci]
                del c[cj]
                centers = np.delete(centers, (ci), axis = 0)
                centers = np.delete(centers, (cj), axis = 0)
                cmerge_idx.remove(ci)
                cmerge_idx.remove(cj)

                nclusters -= 1
                this_comb += 1
            else:
                continue

        iterations += 1

    return (centers, c)

def isodata_test():
    """ Test if algorithm goes right """
        
    x1 = np.array((np.random.randn(100) + 3, np.random.randn(100) * 0.5 + 2)).transpose()
    x2 = np.array((np.random.randn(100), np.random.randn(100) * 0.75 - 1)).transpose()
    x3 = np.array((np.random.randn(100) * 0.4 - 1, np.random.randn(100) * 0.6 + 1)).transpose()
    x = np.vstack([x1, x2, x3])
    x = x[np.random.permutation(x.shape[0])]
    ninit_clusters = 1
    exp_clusters = 4
    theta_n = 75
    theta_s = 0.3
    theta_c = 2
    combL = 20
    max_iters = 1000

    centers, c = cluster_isodata(x, ninit_clusters, theta_n, theta_s, theta_c, exp_clusters, combL, max_iters)

    import matplotlib.pyplot as plt
    f1 = plt.figure(1)
    
    label = np.zeros(x.shape[0])
    for i in xrange(len(c)):
        label[c[i]] = i + 1
    
    plt.scatter(x[:, 0], x[:, 1], 60, 30.0 * label)
    plt.scatter(centers[:, 0], centers[:, 1], s = 80, marker = 'o', color = 'y')

    plt.ylim((-5, 5))
    plt.xlim((-5, 7))
    plt.show()

if __name__ == "__main__":
    isodata_test()
