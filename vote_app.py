import streamlit as st
import sqlite3

# Connect to SQLite database
def connect_db():
    conn = sqlite3.connect('voting.db')
    return conn

# Function to fetch candidates
def get_candidates(position):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT id, name FROM candidates WHERE position = ?', (position,))
    candidates = c.fetchall()
    conn.close()
    return candidates

# Function to cast a vote
def cast_vote(candidate_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute('UPDATE candidates SET votes = votes + 1 WHERE id = ?', (candidate_id,))
    conn.commit()
    conn.close()

# Main voting interface
def main():
    st.title("College Election Voting System")
    
    # Voting options for different positions
    positions = ['President', 'Vice President', 'Secretary', 'Joint Secretary']
    
    for position in positions:
        st.header(f'Vote for {position}')
        candidates = get_candidates(position)
        selected_candidate = st.radio(f'Select your {position}', [name for id, name in candidates])
        
        if st.button(f'Vote for {position}'):
            candidate_id = next(id for id, name in candidates if name == selected_candidate)
            cast_vote(candidate_id)
            st.success(f'Your vote for {selected_candidate} has been recorded!')

    if st.button("View Results"):
        show_results()

# Function to display results
def show_results():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT position, name, votes FROM candidates')
    results = c.fetchall()
    conn.close()
    
    st.header("Election Results")
    for result in results:
        st.write(f'{result[0]}: {result[1]} - {result[2]} votes')

if __name__ == '__main__':
    main()
