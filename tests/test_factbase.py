import pytest
import torch
from factbase import FactBase, create_factbase

class TestFactBase:
    def test_init(self):
        m = FactBase(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = FactBase(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_factbase()
        assert isinstance(m, FactBase)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
