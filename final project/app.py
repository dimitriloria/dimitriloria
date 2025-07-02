from flask import Flask, render_template, request, jsonify
import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Home page - choose waveform type"""
    return render_template('index.html')

@app.route('/waveform')
def waveform():
    """Waveform visualizer page"""
    waveform_type = request.args.get('type', 'sine')
    return render_template('waveform.html', waveform_type=waveform_type)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/generate_waveform', methods=['POST'])
def generate_waveform():
    """API endpoint to generate waveform data"""
    data = request.get_json()
    
    waveform_type = data.get('type', 'sine')
    frequency = float(data.get('frequency', 1))
    amplitude = float(data.get('amplitude', 1))
    phase = float(data.get('phase', 0))
    samples = int(data.get('samples', 1000))
    
    
    t = np.linspace(0, 2/frequency, samples)
    
   
    if waveform_type == 'sine':
        y = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    elif waveform_type == 'square':
        y = amplitude * np.sign(np.sin(2 * np.pi * frequency * t + phase))
    elif waveform_type == 'triangle':
        y = amplitude * (2/np.pi) * np.arcsin(np.sin(2 * np.pi * frequency * t + phase))
    elif waveform_type == 'sawtooth':
        y = amplitude * 2 * (t * frequency - np.floor(t * frequency + 0.5))
    else:
        y = np.zeros_like(t)  
    
  
    time_data = t.tolist()
    amplitude_data = y.tolist()
    
    return jsonify({
        'time': time_data,
        'amplitude': amplitude_data,
        'frequency': frequency,
        'amplitude_value': amplitude,
        'phase': phase,
        'type': waveform_type
    })

@app.route('/api/export_csv', methods=['POST'])
def export_csv():
    """Export waveform data as CSV"""
    data = request.get_json()
    time_data = data.get('time', [])
    amplitude_data = data.get('amplitude', [])
    
    csv_content = "Time,Amplitude\n"
    for t, a in zip(time_data, amplitude_data):
        csv_content += f"{t:.6f},{a:.6f}\n"
    
    return jsonify({'csv': csv_content})

if __name__ == '__main__':
    app.run(debug=True)