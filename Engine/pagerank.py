import numpy as np
import random
import pymysql
import ast
import sys
sys.path.append("C:/My_app/code/咻Search")
from config import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD


class PageRank():
    '''
    G: 传入图的邻接矩阵
    T: 迭代计算次数上限
    eps: 误差上限
    beta: 公式里面的beta
    return: list
    注：误差小于eps或者迭代次数大于T结束迭代计算
    '''
    def __init__(self, G, T=300, eps=1e-6, beta=0.8) -> None:
        self.G = G
        self.N = len(G)
        self.T = T
        self.eps = eps
        self.beta = beta

    
    def GtoM(self, G):
        '''
        创建概率转换矩阵
        '''
        M = np.zeros((self.N, self.N))
        for i in range(self.N):
            D_i = sum(G[i])
            if D_i == 0:
                continue
            for j in range(self.N):
                M[j][i] = G[i][j] / D_i  #归一化并转置
        return M
    
    def computePR(self, M):
        '''
        计算PR值
        '''
        R = np.ones(self.N) / self.N
        teleport = np.ones(self.N) / self.N
        for time in range(self.T):
            A = self.beta * M + (1-self.beta)*teleport
            R_new = np.dot(A, R)
            if np.linalg.norm(R_new - R) < self.eps:
                break
            R = R_new.copy()
        return np.around(R_new, 5)
    
    def getPR(self):
        M = self.GtoM(self.G)
        return self.computePR(M)
    
def urls2G():
    '''
    将数据库中urls的关系转化为图
    '''
    # 连接数据库
    # 加上charset='utf8'，避免 'latin-1' encoding 报错等问题
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, 
                        db=MYSQL_DBNAME, charset='utf8')
    # 创建cursor
    cursor_blogs = conn.cursor()
    cursor_list = conn.cursor()
    sql_blogs = 'SELECT page_url, urls FROM search_blogs;'
    sql_list = 'SELECT page_url, urls FROM search_blogs;'
    # 执行sql语句
    cursor_blogs.execute(sql_blogs)
    cursor_list.execute(sql_list)
    # 获取全部查询信息
    re_blogs = cursor_blogs.fetchall()
    re_list = cursor_list.fetchall()
    
    # 将获取的元组信息转换为图
    blogs_index = [url[0] for  url in re_blogs]
    blogs_point = [ast.literal_eval(url[1]) for  url in re_blogs]
    
    list_index = [url[0] for  url in re_list]
    list_point = [ast.literal_eval(url[1]) for  url in re_list]
    indexs = blogs_index + list_index
    points = blogs_point + list_point
    G = np.zeros((len(indexs), len(indexs)))
    for i, index in enumerate(indexs):
        # 依次判断包含的url是是否在爬取过的列表中，有些广告之类的链接页会包含，但没爬取
        for p_url in points[i]:
            try:
                p_index = indexs.index(p_url)
            except:
                p_index = -1
            if p_index != -1:
                G[i][p_index] = 1
                
    return G
    
if __name__ == "__main__":
    # def create_data(N, alpha=0.5): 
    #     G = np.zeros((N, N))
    #     for i in range(N):
    #         for j in range(N):
    #             if i == j:
    #                 continue
    #             if random.random() < alpha:
    #                 G[i][j] = 1
    #     return G
    # G = create_data(10)
    # PR = PageRank(G)
    # print(PR.getPR())
    G = urls2G()
    print(type(G))
    PR = PageRank(G)
    print(PR.getPR())