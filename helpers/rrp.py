def plot_rrp():
    ind = stf.get_selected_indices()
    #base = np.mean(stf.get_trace()[stf.get_base_start():stf.get_base_end()])
    base = int(stf.get_base_end())
    x = np.arange(base)
    trace_x = np.arange(len(stf.get_trace())*2)
    
    charge = [0]
    for i in ind:
        
        if i == ind[-1]:
            break
        trace = stf.get_trace(trace=i)
        trace = np.hstack((trace, stf.get_trace(trace=i+1)))
        baseline = trace[:base]
        fit = np.polyfit(x, baseline, 1)
        
        line = fit[0]*trace_x + fit[1]
        trace = trace-line
        
        total = np.sum(trace[base:])
        
        if total > 0:
            charge.append(0)
        else:
            charge.append(-total)
        
    charge = np.array(charge)
    x = np.arange(82, 100)
    charge_sum = np.cumsum(charge)
    charge_end = charge_sum[-18:]
    fit = np.polyfit(x, charge_end, 1)
    line = fit[0]*np.arange(100) + fit[1]
    rrp = fit[1]
    
    fig, ax = plt.subplots()
    ax.plot(charge_sum)
    ax.plot(line)
    plt.show()
    
    baseline = np.median(stf.get_trace(trace=0)[:base])
    first = -np.sum(stf.get_trace(trace=0) - baseline)
    release_prob = first/rrp
    return_vals = {'first_charge': first, 'pool_size': rrp, 'P_r': release_prob}
    stf.show_table(return_vals)
    
    return {'first_charge': first, 'pool_size': rrp, 'P_r': release_prob}
    
    
def plot_rrp():
    ind = stf.get_selected_indices()
    #base = np.mean(stf.get_trace()[stf.get_base_start():stf.get_base_end()])
    base = stf.get_base_end()
    x = np.arange(base)
    trace_x = np.arange(len(stf.get_trace()))
    baseline = np.median(stf.get_trace(trace=0)[:base])
    
    charge = [0]
    for i in ind:

        trace = stf.get_trace(trace=i)
        trace = trace-baseline
        
        total = np.sum(trace)
        
        if total > 0:
            charge.append(0)
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
    
    first = -np.sum(stf.get_trace(trace=0) - baseline)
    release_prob = first/rrp
    return_vals = {'first_charge': first, 'pool_size': rrp, 'P_r': release_prob}
    
    stf.show_table(return_vals)
    
    return {'first_charge': first, 'pool_size': rrp, 'P_r': release_prob}
        
