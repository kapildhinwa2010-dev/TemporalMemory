import pytest
import torch
from temporalmemory import TemporalMemory, create_temporalmemory

class TestTemporalMemory:
    def test_init(self):
        m = TemporalMemory(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = TemporalMemory(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_temporalmemory()
        assert isinstance(m, TemporalMemory)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
