batch_sizes = [4, 16, 128]

def get_iterations(starting_size, batch_size, compute_budget):
    compute_budget_without_starting_size = compute_budget - starting_size

    iterations_without_start = compute_budget_without_starting_size // batch_size

    if (iterations_without_start) == 0:
        raise Exception(f"Compute budget is not compatible with batch_size {batch_size} and starting_size {starting_size}")


    return iterations_without_start

number_of_reruns = 5

generators = ['monte-carlo', 'sobol']

def make_prefix_main(*, batch_size,
                starting_size,
                     rerun,
                     generator):
    return '{generator}_{batch_size}_{starting_size}_{rerun}'.format(
        batch_size=batch_size, starting_size=starting_size,
        rerun=rerun,
        generator=generator)

def make_prefix_competitor(*, batch_size,
                           starting_size,
                           rerun,
                           iteration,
                           generator):
    return 'competitor_{generator}_{batch_size}_{starting_size}_{rerun}_{iteration}'.format(
        batch_size=batch_size, starting_size=starting_size,
        rerun=rerun,
        iteration=iteration,
        generator=generator)

def get_objective_filename(*, batch_size,
                           starting_size,
                           rerun,
                           iteration,
                           generator):
    return "{}objective_{}.txt".format(make_prefix_main(batch_size=batch_size,
                                                        generator=generator,
                                                        starting_size=starting_size,
                                                        rerun=rerun),
                                       iteration)

def get_competitor_objective_filename(*, batch_size,
                                      starting_size,
                                      rerun,
                                      iteration,
                                      pass_number,
                                      generator):
    
    return "{}objective_{}.txt".format(make_prefix_competitor(batch_size=batch_size,
                                                        starting_size=starting_size,
                                                              rerun=rerun,
                                                              generator=generator,
                                                              iteration=iteration),
                                       pass_number)


def make_starting_sizes(batch_size, compute_budget):
    starting_sizes = [batch_size]
    while 2 * batch_size < compute_budget:
        starting_sizes.append(2 * batch_size)
        batch_size = 2 * batch_size

    return starting_sizes
    
