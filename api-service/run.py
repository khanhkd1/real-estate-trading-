from app import app
import pickle

bayesian_ridge_model = pickle.load(open('services/bayesian_ridge_model/bayesian_ridge_model.pkl', 'rb'))
address_encode = pickle.load(open('services/bayesian_ridge_model/address_encode.pkl', 'rb'))
investor_encode = pickle.load(open('services/bayesian_ridge_model/investor_encode.pkl', 'rb'))

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
