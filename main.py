from flask import Flask, request, redirect, url_for, render_template_string, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Öğrenci bilgileri
student_info = {
    'name': 'Harun',
    'surname': 'Yiğit',
    'student_number': '211220029'
}

# Dosya yolları
excel_file_path = 'static/odev6hrn.xlsx'
plot_image_path = 'static/odev6hrn.jpeg'


def generate_random_coordinates(num_points, min_val=0, max_val=1000):
    x_coords = np.random.randint(min_val, max_val + 1, num_points)
    y_coords = np.random.randint(min_val, max_val + 1, num_points)
    return x_coords, y_coords


def save_to_excel(df, file_path):
    df.to_excel(file_path, index=False)


def create_dataframe(x_coords, y_coords):
    return pd.DataFrame({'X Koordinatları': x_coords, 'Y Koordinatları': y_coords})


def plot_coordinates(x_coords, y_coords, grid_size, plot_path):
    num_colors = (1000 // grid_size) ** 2
    colors = plt.get_cmap('tab20', num_colors)

    plt.figure(figsize=(10, 10))
    for i in range(0, 1000, grid_size):
        for j in range(0, 1000, grid_size):
            mask = (x_coords >= i) & (x_coords < i + grid_size) & (y_coords >= j) & (y_coords < j + grid_size)
            plt.scatter(x_coords[mask], y_coords[mask],
                        color=colors((i // grid_size) * (1000 // grid_size) + (j // grid_size)),
                        label=f'Grid ({i},{j})')

    plt.xlabel('X Koordinatları')
    plt.ylabel('Y Koordinatları')
    plt.grid(True)
    plt.savefig(plot_path)
    plt.close()


@app.route('/')
def index():
    return render_template('index.html', student_info=student_info, plot_image_path=plot_image_path)


@app.route('/generate', methods=['POST'])
def generate():
    num_points = 500
    grid_size = 200

    x_coords, y_coords = generate_random_coordinates(num_points)

    df = create_dataframe(x_coords, y_coords)
    save_to_excel(df, excel_file_path)

    plot_coordinates(x_coords, y_coords, grid_size, plot_image_path)

    return redirect(url_for('index'))


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')

    # İlk görseli oluştur
    num_points = 500
    grid_size = 200
    x_coords, y_coords = generate_random_coordinates(num_points)
    df = create_dataframe(x_coords, y_coords)
    save_to_excel(df, excel_file_path)
    plot_coordinates(x_coords, y_coords, grid_size, plot_image_path)

    app.run(debug=True)
