batch_sizes = [4, 16, 128]
iterations = 8

number_of_reruns = 2

def make_prefix_main(*, batch_size,
                starting_size,
                rerun):
    return '{batch_size}_{starting_size}_{rerun}'.format(
        batch_size=batch_size, starting_size=starting_size,
        rerun=rerun)

def make_prefix_competitor(*, batch_size,
                           starting_size,
                           rerun,
                           iteration):
    return 'competitor_{batch_size}_{starting_size}_{rerun}_{iteration}'.format(
        batch_size=batch_size, starting_size=starting_size,
        rerun=rerun,
        iteration=iteration)

def get_objective_filename(*, batch_size,
                           starting_size,
                           rerun,
                           iteration):
    return "{}objective_{}.txt".format(make_prefix_main(batch_size=batch_size,
                                                        starting_size=starting_size,
                                                        rerun=rerun),
                                       iteration)

def get_competitor_objective_filename(*, batch_size,
                                      starting_size,
                                      rerun,
                                      iteration,
                                      pass_number):
    
    return "{}objective_{}.txt".format(make_prefix_competitor(batch_size=batch_size,
                                                        starting_size=starting_size,
                                                              rerun=rerun,
                                                              iteration=iteration),
                                       pass_number)


def make_starting_sizes(batch_size):
    return [batch_size, 2*batch_size]#, 4*batch_size, 8*batch_size]
    
