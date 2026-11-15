"""
TemporalMemory: Temporal memory system

Professional implementation of TemporalMemory for research and production use.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Dict, Any
import warnings

warnings.filterwarnings('ignore')


class TemporalMemory(nn.Module):
    """
    TemporalMemory - Temporal memory system

    Args:
        dim: Input dimension
        hidden_dim: Hidden dimension  
        num_layers: Number of layers
        dropout: Dropout rate
    """

    def __init__(
        self,
        dim: int = 256,
        hidden_dim: int = 512,
        num_layers: int = 2,
        dropout: float = 0.1
    ):
        super().__init__()
        self.dim = dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout

        self.layers = nn.ModuleList()
        for i in range(num_layers):
            in_dim = dim if i == 0 else hidden_dim
            out_dim = dim if i == num_layers - 1 else hidden_dim
            self.layers.append(nn.Linear(in_dim, out_dim))
            if i < num_layers - 1:
                self.layers.append(nn.SiLU())
                self.layers.append(nn.Dropout(dropout))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        for layer in self.layers:
            x = layer(x)
        return x

    def get_config(self) -> Dict[str, Any]:
        """Get configuration."""
        return {
            'dim': self.dim,
            'hidden_dim': self.hidden_dim,
            'num_layers': self.num_layers,
            'dropout': self.dropout
        }


def create_temporalmemory(
    dim: int = 256,
    hidden_dim: int = 512,
    num_layers: int = 2,
    dropout: float = 0.1
) -> TemporalMemory:
    """
    Factory function to create TemporalMemory instance.
    """
    return TemporalMemory(
        dim=dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
        dropout=dropout
    )


__all__ = ['TemporalMemory', 'create_temporalmemory']
