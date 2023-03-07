#store.py
from kivyredux import State, Store, Action, Reducer
main_s = State(first_time=True)

def main_state_rd(action,s=main_s):
    if(action.type=='toggle_first_time'):
        p_first_time = s.get("first_time")
        s.update("first_time",not p_first_time)

first_time_toggle_action = Action(action_type="toggle_first_time")
main_rd = Reducer(reducer_cb=main_state_rd)
main_store = Store(reducers=[main_state_rd],state=main_s)