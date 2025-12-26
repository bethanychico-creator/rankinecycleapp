#!/usr/bin/env python3
import sys
import json
import CoolProp.CoolProp as CP

def calculate_rankine_cycle(P3, T3, P4, T5, P6):
    """
    Calculate 6-state Rankine cycle with reheat
    
    Args:
        P3: Pressure at state 3 in Pa
        T3: Temperature at state 3 in K
        P4: Pressure at state 4 in Pa
        T5: Temperature at state 5 in K
        P6: Pressure at state 6 in Pa
    
    Returns:
        Dictionary with all states, energy balance, and results
    """
    
    # State 3 (HP turbine inlet)
    h3 = CP.PropsSI('H', 'P', P3, 'T', T3, 'water')
    s3 = CP.PropsSI('S', 'P', P3, 'T', T3, 'water')
    
    # State 4 (HP turbine outlet) - isentropic expansion
    s4 = s3
    T4 = CP.PropsSI('T', 'S', s4, 'P', P4, 'water')
    h4 = CP.PropsSI('H', 'S', s4, 'P', P4, 'water')
    
    # State 5 (LP turbine inlet) - after reheating
    P5 = P4
    h5 = CP.PropsSI('H', 'T', T5, 'P', P5, 'water')
    s5 = CP.PropsSI('S', 'T', T5, 'P', P5, 'water')
    
    # State 6 (LP turbine outlet) - isentropic expansion
    s6 = s5
    T6 = CP.PropsSI('T', 'P', P6, 'S', s6, 'water')
    h6 = CP.PropsSI('H', 'P', P6, 'S', s6, 'water')
    X6 = CP.PropsSI('Q', 'P', P6, 'S', s6, 'water')  # Quality
    
    # State 1 (Condenser outlet) - saturated liquid
    X1 = 0  # Saturated liquid
    P1 = P6
    T1 = CP.PropsSI('T', 'P', P1, 'Q', X1, 'water')
    h1 = CP.PropsSI('H', 'P', P1, 'Q', X1, 'water')
    s1 = CP.PropsSI('S', 'P', P1, 'Q', X1, 'water')
    
    # State 2 (Pump outlet) - isentropic compression
    P2 = P3
    s2 = s1
    T2 = CP.PropsSI('T', 'S', s2, 'P', P2, 'water')
    h2 = CP.PropsSI('H', 'S', s2, 'P', P2, 'water')
    
    # Energy Balance
    w_pump = h2 - h1
    q_in1 = h3 - h2
    w_turb1 = h3 - h4
    q_in2 = h5 - h4
    w_turb2 = h5 - h6
    q_out = h6 - h1
    
    # Required System Parameters
    w_net = w_turb1 + w_turb2 - w_pump
    q_total = q_in1 + q_in2
    eta_th = (w_net / q_total) * 100
    
    # Check if state 4 is in two-phase region
    try:
        X4 = CP.PropsSI('Q', 'P', P4, 'S', s4, 'water')
        if X4 >= 0 and X4 <= 1:
            x4 = X4
        else:
            x4 = None
    except:
        x4 = None
    
    return {
        'states': {
            'state1': {'P': P1, 'T': T1, 'h': h1, 's': s1, 'x': X1},
            'state2': {'P': P2, 'T': T2, 'h': h2, 's': s2, 'x': None},
            'state3': {'P': P3, 'T': T3, 'h': h3, 's': s3, 'x': None},
            'state4': {'P': P4, 'T': T4, 'h': h4, 's': s4, 'x': x4},
            'state5': {'P': P5, 'T': T5, 'h': h5, 's': s5, 'x': None},
            'state6': {'P': P6, 'T': T6, 'h': h6, 's': s6, 'x': X6},
        },
        'energy': {
            'w_pump': w_pump,
            'q_in1': q_in1,
            'w_turb1': w_turb1,
            'q_in2': q_in2,
            'w_turb2': w_turb2,
            'q_out': q_out,
        },
        'results': {
            'w_net': w_net,
            'q_total': q_total,
            'eta_th': eta_th,
        }
    }

if __name__ == '__main__':
    # Read inputs from command line arguments
    if len(sys.argv) != 6:
        print("Usage: python rankine_calculator.py P3 T3 P4 T5 P6")
        sys.exit(1)
    
    try:
        P3 = float(sys.argv[1])  # Pa
        T3 = float(sys.argv[2])  # K
        P4 = float(sys.argv[3])  # Pa
        T5 = float(sys.argv[4])  # K
        P6 = float(sys.argv[5])  # Pa
        
        result = calculate_rankine_cycle(P3, T3, P4, T5, P6)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)
