def plot_rrp():
    ind = stf.get_selected_indices()
    #base = np.mean(stf.get_trace()[stf.get_base_start():stf.get_base_end()])
    base = stf.get_base_end()
    x = np.arange(base)
    trace_x = np.arange(len(stf.get_trace()))
    
    charge = [0]
    for i in ind:

        trace = stf.get_trace(trace=i)
        baseline = trace[:base]
        fit = np.polyfit(x, baseline, 1)
        
        line = fit[0]*trace_x + fit[1]
        trace = trace-line
        
        total = np.sum(trace)
        
        if total > 0:
            charge.append(0)
            #fig, ax = plt.subplots()
            #ax.plot(trace)
            #ax.plot(line)
            #plt.show()
        else:
            charge.append(total)
        
    charge = -np.array(charge)
    x = np.arange(91, 101)
    charge_sum = np.cumsum(charge)
    charge_end = charge_sum[-10:]
    fit = np.polyfit(x, charge_end, 1)
    line = fit[0]*np.arange(100) + fit[1]
    rrp = fit[1]
    
    fig, ax = plt.subplots()
    ax.plot(charge_sum)
    ax.plot(line)
    plt.show()
    
    return rrp
        
