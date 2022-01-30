from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from app.api.models import RoutingInput
from app.api.helpers import Helper

class RoutingEngine():
  def __init__(self, routing_input_payload: RoutingInput):
    helper = Helper()

    vehicles = routing_input_payload.vehicles
    jobs = routing_input_payload.jobs
    matrix = routing_input_payload.matrix

    self.data_model = helper.create_data_model(vehicles, jobs, matrix)
  
  def get_vehicle_id_of_vehicle(self, vehicle):
    """ Map vehicles with vehicle ids which is basically +1 in this case. """

    return vehicle + 1
    
  def get_job_id_of_node(self, node):
    """ Map nodes with job ids. """

    job = next(filter(lambda job: job.location_index == node, self.data_model["jobs"]), None)

    if job == None:
      return 0
    else:
      return job.id
  
  def get_solution_output(self, manager, routing, solution):
    """ Get the output of the optimizer in formatted way. """

    output = {"total_duration": 0, "routes": {}} 
    total_duration = 0
    
    for vehicle in range(self.data_model['num_vehicles']):
      vehicle_id = self.get_vehicle_id_of_vehicle(vehicle)
      output['routes'][f"{vehicle_id}"] = {"jobs": [], "duration": 0}

      duration = 0

      index = routing.Start(vehicle)
      node = manager.IndexToNode(index)
      job_id = self.get_job_id_of_node(node)
      output['routes'][f"{vehicle_id}"]["jobs"].append(str(job_id))

      while not routing.IsEnd(index):
          previous_index = index
          index = solution.Value(routing.NextVar(index))
          node = manager.IndexToNode(index)
          job_id = self.get_job_id_of_node(node)

          duration += routing.GetArcCostForVehicle(previous_index, index, vehicle)
          
          if job_id != 0:
            output['routes'][f"{vehicle_id}"]["jobs"].append(str(job_id))

      output['routes'][f"{vehicle_id}"]["duration"] = duration

      total_duration += duration

    output["total_duration"] = total_duration

    return output

  def optimize(self):
    """ Solve the problem. """

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(self.data_model['duration_matrix']), self.data_model['num_vehicles'], self.data_model['start_indices'], self.data_model['end_indices'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Duration Callback for Arc Cost
    def duration_callback(from_index, to_index):
      """ Returns the duration between the two nodes. """

      from_node = manager.IndexToNode(from_index)
      to_node = manager.IndexToNode(to_index)

      return self.data_model['duration_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(duration_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Track Demands For Capacity Management
    def demand_callback(from_index):
      """ Returns the demand of the node. """
      from_node = manager.IndexToNode(from_index)

      return self.data_model['demands'][from_node]
    
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
      demand_callback_index,
      0,
      self.data_model['vehicle_capacities'], 
      True,
      'Capacity')
    
    # Allow to drop nodes without demand.
    penalty = 0
    for node in range(0, len(self.data_model['duration_matrix'])):
      if (self.data_model["demands"] != 0):
        penalty = int(10e9)

      if (node in self.data_model["start_indices"]) or (node in self.data_model["end_indices"]):
        continue
        
      routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

    # Setting search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(2)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Get and return solution.
    if solution:
      output = self.get_solution_output(manager, routing, solution)
      return output
    else:
      return {"total_duration": 0, "routes": {}} 