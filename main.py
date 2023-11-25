from flask import Flask, render_template, request, session
from forms.login_form import LoginForm
from forms.signup_form import SignupForm
from forms.add_election import AddElectionForm
from forms.add_candidate import AddCandidateForm
from flask import redirect, url_for
import pandas as pd
import numpy as np
from utils import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    
    email = session.get('email')
    if email:
        if request.method == 'GET':

            # checking if the user is a government employee or a citizen
            email_domain = email.split("@")[1]

            if email_domain == "government.it":
                account = account_government
            else:
                account = account_citizens
            encoded_email = string_to_bytes32(email)

            # Call the contract function
            user_info = user_contract.functions.getUserInfo(encoded_email).call({
                "from": account,
            })

            # Now 'user_info' contains the returned values from the contract function
            name, lastname, is_admin = user_info

            # Convert bytes32 to string
            name = bytes32_to_string(name)
            lastname = bytes32_to_string(lastname)
            user = {
                'name': name,
                'lastname': lastname,
                'email': email, 
                'is_admin': is_admin
            }
            if is_admin:
                elections = get_all_elections()
                form_add_election = AddElectionForm()
                return render_template('index_government.html', 
                                       user=user, 
                                       email=email, 
                                       elections=elections, 
                                       form_add_election=form_add_election
                                       )
            else:
                elections = get_all_elections()
                form_add_election = AddElectionForm()
                return render_template('index.html', 
                                       user=user, 
                                       email=email, 
                                       elections=elections, 
                                       form_add_election=form_add_election
                                       )
        else:
            request_form = request.form.to_dict(flat=False)
            id = request_form['id'][0]
            purpose = request_form['purpose'][0]
            message = add_election(id, purpose)
            print(message)
            return redirect(url_for('homepage'))

    else:
        message = "In order to access the homepage, please log in!"
        form_login = LoginForm()
        return render_template('login.html', form_login=form_login, message=message)


@app.route('/election_details/<int:id_election>', methods=['GET', 'POST'])
def election_details(id_election):
    email = session.get('email')
    user = get_user_info(email)
    if email:
        if request.method == 'GET':
            election = get_election_info(id_election)
            raw_candidates = get_all_candidates()

            candidates = []
            for raw_candidate in raw_candidates:

                id_candidate = raw_candidate[0]
                name = bytes32_to_string(raw_candidate[1])
                lastname = bytes32_to_string(raw_candidate[2])
                manifesto = bytes32_to_string(raw_candidate[3])
                votes = raw_candidate[4]
                election_id = raw_candidate[5]

                candidate = {
                    'id_candidate': id_candidate,
                    'name': name,
                    'lastname': lastname,
                    'manifesto': manifesto, 
                    'votes': votes,
                    'election_id': election_id
                }
                candidates.append(candidate)

            # checking if the current user already voted
            has_voted = check_if_user_voted(email, id_election)

            form_add_candidate = AddCandidateForm()
            message=f"In order to avoid unexpected errors, please type the following id candidate: {len(candidates)+1}"
            return render_template('election_page.html', 
                                   election=election, 
                                   candidates=candidates, 
                                   user=user, 
                                   form_add_candidate=form_add_candidate, 
                                   message=message,
                                   has_voted = has_voted,
                                   email=email
                                   )
        else:
            request_form = request.form.to_dict(flat=False)
            election_id = request_form['electionId'][0]
            purpose = request_form['purpose'][0]

            # Check if 'expired' key is present in the form data
            expired = request_form.get('expired', [False])[0]  # Default to False if 'expired' is not present

            purpose = string_to_bytes32(purpose)
            expired = bool(expired)
            # update description
            update_election_purpose(election_id, purpose)
            # update expiration
            update_election_expired(election_id, expired)
            return redirect(url_for('election_details', id_election=id_election))
    else:
        return redirect(url_for('user_login'))

    

@app.route('/add_candidate/<int:id_election>', methods=['POST'])
def add_candidate(id_election):

    email = session.get('email')
    if email:
        request_form = request.form.to_dict(flat=False)
        id = request_form['id'][0]
        name = request_form['name'][0]
        lastname = request_form['lastname'][0]
        manifesto = request_form['manifesto'][0]

        id_election = int(id_election)

        response = add_candidate_to_election(id, name, lastname, manifesto, id_election)
        if response:
            return redirect(url_for('election_details', id_election=id_election))
        else:
            election = get_election_info(id_election)
            candidates = get_all_candidates()
            form_add_candidate = AddCandidateForm()

            email = session.get('email')
            user = get_user_info(email)

            message = f"ERROR DURING CANDIDATE CREATION: PLEASE, BE SURE YOU TYPED A CORRECT CANDIDATE ID. THE RIGHT ID TO INSERT IS: {len(candidates)}"
            return render_template('election_page.html', 
                                   election=election, 
                                   candidates=candidates, 
                                   user=user, 
                                   form_add_candidate=form_add_candidate, 
                                   message=message,
                                   email=email
                                   )
    else:
        return redirect(url_for('user_login'))
    

    
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    email = session.get('email')
    
    if request.method == 'GET':

        if email: # if user is logged

            return redirect(url_for('homepage'))
        else:
            message = "In order to access the homepage, please log in!"
            form_login = LoginForm()
            return render_template('login.html', form_login=form_login, message=message)
        
    else:
        request_form = request.form.to_dict(flat=False)
        email = request_form['email'][0]
        password = request_form['password'][0]

        # checking if the user is a government employee or a citizen
        email_domain = email.split("@")[1]

        if email_domain == "government.it":
            account = account_government
        else:
            account = account_citizens

        # Encode username and password as bytes32
        encoded_email = string_to_bytes32(email)
        encoded_password = string_to_bytes32(password)

        transaction = user_contract.functions.login(encoded_email, encoded_password).build_transaction({
            "from": account,
            'gas': 200000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            "nonce": web3.eth.get_transaction_count(account),
        })

        try:
            # Send the transaction
            transaction_hash = web3.eth.send_transaction(transaction)

            # Wait for the transaction to be mined
            receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

            if receipt["status"] == 1:

                session['email'] = email
                return redirect(url_for('homepage'))

            else:
                message = "Email or password are incorrect! If you did not register yet, click on the link under the form."
                form_login = LoginForm()
                return render_template('login.html', form_login=form_login, message=message)
        except ValueError:
            message = "Email or password are incorrect! If you did not register yet, click on the link under the form."
            form_login = LoginForm()
            return render_template('login.html', form_login=form_login, message=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup_user():

    if request.method == 'GET':

        email = session.get('email')

        if email: # if user is logged

            return redirect(url_for('homepage'))
        else:
            form_signup = SignupForm()
            return render_template('signup.html', form_signup=form_signup, message="")
    
    else:
        request_form = request.form.to_dict(flat=False)

        name = request_form['name'][0]
        lastname = request_form['lastname'][0]
        email = request_form['email'][0]
        password = request_form['password'][0]

        email_domain = email.split("@")[1]

        if email_domain == "government.it":
            account = account_government
            is_admin = True
        else:
            account = account_citizens
            is_admin = False

        # Encode user information as bytes32
        encoded_name = string_to_bytes32(name)
        encoded_lastname = string_to_bytes32(lastname)
        encoded_email = string_to_bytes32(email)
        encoded_password = string_to_bytes32(password)

        transaction = user_contract.functions.register(encoded_name, encoded_lastname, encoded_email, encoded_password, is_admin).build_transaction({
            "from": account,
            'gas': 200000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            "nonce": web3.eth.get_transaction_count(account),
        })
        try:
            # Send the transaction
            transaction_hash = web3.eth.send_transaction(transaction)

            # Wait for the transaction to be mined
            receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

            if receipt["status"] == 1:
                return redirect(url_for('user_login'))
            else:
                message = "User already registered! Please, log in."
                form_login = LoginForm()
                return render_template('login.html', form_login=form_login, message=message)

        except ValueError:
            message = "User already registered! Please, log in."
            form_login = LoginForm()
            return render_template('login.html', form_login=form_login, message=message)


@app.route('/logout_user')
def logout_user():
    # Clear user information from the session
    session.pop('email', None)
    return redirect(url_for('user_login'))


# Define the route for voting
@app.route('/vote_candidate/<int:id_election>/<int:candidate_id>')
def vote_candidate(id_election, candidate_id):
    email = session.get('email')
    if email:
        result = vote_candidate_by_election(email, candidate_id, id_election)
        if result:
            print("Voted!!")
        else:
            print("The current user already voted in this election!")

        return redirect(url_for('election_details', id_election=id_election))
    else:
        return redirect(url_for('user_login'))
            


if __name__ == '__main__':
    # set up the variable regarding the secret key in this app
    app.config['SECRET_KEY'] = "SECRET"
    app.run(debug=True, port=5505)