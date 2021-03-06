import torch
import os, sys
import numpy as np

from bindsnet.network          import *
from bindsnet.network.nodes    import *
from bindsnet.network.monitors import Monitor


class TestNodes:
	'''
	Tests all stable groups of neurons / nodes.
	'''
	def test_init(self):
		for nodes in [Input,
					  McCullochPitts,
					  IFNodes,
					  LIFNodes,
					  AdaptiveLIFNodes]:
			for n in [1, 100, 10000]:
				layer = nodes(n)
				
				assert layer.n == n
				assert all(layer.s.float() == torch.zeros(n))
				
				if nodes in [LIFNodes,
							 AdaptiveLIFNodes]:
					assert all(layer.v == layer.rest * torch.ones(n))

				layer = nodes(n, traces=True, trace_tc=1e-5)
				
				assert layer.n == n; assert layer.trace_tc == 1e-5
				assert all(layer.s.float() == torch.zeros(n)); assert all(layer.x == torch.zeros(n))
				assert all(layer.x == torch.zeros(n))
				
				if nodes in [LIFNodes,
							 AdaptiveLIFNodes]:
					assert all(layer.v == layer.rest * torch.ones(n))

		for nodes in [LIFNodes,
					  AdaptiveLIFNodes]:
			for n in [1, 100, 10000]:
				layer = nodes(n, rest=0.0, reset=-10.0, thresh=10.0, refrac=3, decay=7e-4)
				
				assert layer.rest == 0.0; assert layer.reset == -10.0; assert layer.thresh == 10.0
				assert layer.refrac == 3; assert layer.decay == 7e-4
				assert all(layer.s.float() == torch.zeros(n))
				assert all(layer.v == layer.rest * torch.ones(n))
