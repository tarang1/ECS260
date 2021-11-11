from sklearn.preprocessing import PolynomialFeatures

def PolynomialRegression(X, y, deg=2, figsize=7):
    
    print(X.shape, type(X))
    print(y.shape, type(y))

    X = np.sort(X)
    y = np.sort(y)
    
    X = X.reshape(-1,1)
    print(X.shape, type(X))

    y = y.reshape(-1,1)
    print(y.shape, type(y))

    
    #print(X)
    
    poly = PolynomialFeatures(degree=deg, include_bias=False)
    X_poly = poly.fit_transform(X)
    
    # This exactly implements the above formula
    polyReg = LinearRegression().fit(X_poly, y) 
    
    '''
    # Printing Coefficients
    coef = pd.DataFrame(polyReg.coef_, columns=[f'b{i+1}' for i in range(deg)])
    coef.insert(loc=0, column='b0', value=polyReg.intercept_)
    coef = coef.style.format("{:10,.10f}") # Comment this out to not suppressing the scientific notation
    display(coef)
    '''
    #### Plotting ####
    #plt.figure(figsize=(figsize, figsize))
    plt.scatter(X, y, alpha=.5)
    plt.plot(np.sort(X), polyReg.predict(X_poly), color='tab:red', alpha=.5)

    
    plt.show()
    
    
def plot_model(dict) :
  for k in dict.keys() :
    x = []
    y = []
    for i in dict[k]['contributors']:
      j = 0
      print(i)
      if 'lifespan' not in dict[k]['contributors'][i] :
        dict[k]['contributors'][i]['lifespan'] = -1
      if 'commits' not in dict[k]['contributors'][i] :
        dict[k]['contributors'][i]['commits'] = -1
      
      if i == 'ctan888' :
        print(dict[k]['contributors'][i])
      print(j, dict[k]['contributors'][i]['lifespan'])
      #print(dict['apache/kafka']['contributors'][i]['lifespan'])
      x.append(dict[k]['contributors'][i]['lifespan'])
      y.append(dict[k]['contributors'][i]['commits'])
      j += 1
    PolynomialRegression(np.asarray(x), np.asarray(y), deg = 10)

  return x,y


def plot_issues_model(dict) :
  x = []
  y = []

  for k in dict.keys() :
    y.append(dict[k]['issues'])
    x.append(len(dict[k]['contributors'].items()))

  PolynomialRegression(np.asarray(x), np.asarray(y), deg = 4)

  return x,y
