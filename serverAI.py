import socket
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import time


class ServerAI:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port

    def start_server(self):
        # Create a socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)

        print("The server has been started. Waiting for client connection...")

        # Accept connection
        client_socket, addr = server_socket.accept()
        print(f"{addr} is connected.")

        # Collect data
        data = []
        try:
            start_time = time.time()
            while time.time() - start_time < 60:  # Collect data for 1 minute
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Received Data : {message}")
                data.append(float(message))
        finally:
            client_socket.close()
            server_socket.close()

        # Convert data to DataFrame and create target variable
        df = pd.DataFrame(data, columns=['feature'])
        df['target'] = df['feature'] ** 2 + 5 * df['feature'] + 3  # Create a more complex target variable

        # Data preprocessing and model training
        X_train, X_test, y_train, y_test = train_test_split(df[['feature']], df['target'], test_size=0.2,
                                                            random_state=42)
        model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
        model.fit(X_train, y_train)

        # Test model performance and print results
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        print(f"Model MSE     : {mse}")
        print(f"Model R2 Score: {r2}")


# Create an instance of ServerAI and start the server
server = ServerAI()
server.start_server()
