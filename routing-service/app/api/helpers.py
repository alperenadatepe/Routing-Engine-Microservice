class Helper:
  def __init__(self):
    pass

  def get_demands(self, matrix, jobs):
    """ Get demand of each job by summing up of the load quantity. """
    demands = [0] * len(matrix)
    for job in jobs:
      demands[job.location_index] = job.load

    return demands

  def get_capacities(self, vehicles):
    """ Get capacity of each vehicle by summing up the given capacity. """
    capacities = [vehicle.capacity for vehicle in vehicles]

    return capacities
    
  def get_start_indices(self, vehicles):
    """ Get start index of each vehicle. """
    start_indices = [vehicle.start_index for vehicle in vehicles]

    return start_indices

  def integrate_end_indices(self, matrix):
    """ Integrate dummy end indices to make the problem open-ended. """

    new_matrix = []
    for row in matrix:
      new_row = row + [0]
      new_matrix.append(new_row)
    
    new_matrix.append([0 for i in new_row])
    
    return new_matrix

  def get_end_indices(self, matrix, start_indices):
    """ 
      Get end index for each vehicle which is a dummy index that has 0 cost to any node. 
      For getting arbitrary ending locations. 
    """
    return [len(matrix) - 1 for i in start_indices]

  def create_data_model(self, vehicles, jobs, matrix):
    """ Creates the data model for the problem. """

    matrix = self.integrate_end_indices(matrix)
    
    demands = self.get_demands(matrix, jobs)
    capacities = self.get_capacities(vehicles)
    start_indices = self.get_start_indices(vehicles)
    end_indices = self.get_end_indices(matrix, start_indices)
    
    data = {}

    data['duration_matrix'] = matrix
    data['demands'] = demands
    data['vehicle_capacities'] = capacities
    data['start_indices'] = start_indices
    data['end_indices'] = end_indices
    data['jobs'] = jobs
    data['num_vehicles'] = len(capacities)

    return data
