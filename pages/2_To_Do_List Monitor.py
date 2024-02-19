import streamlit as st
import pandas as pd 
from db_funcs import *
from PIL import Image
import plotly.express as px 

completed_tasks = 0

def color_df(val):
	if val == "Done":
		color = "green"
		global completed_tasks
		completed_tasks+=1
	elif val == "Doing":
		color = "orange"
	else:
		color = "red"

	return f'background-color: {color}'

st.set_page_config(
    page_title="ToDo",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

top_image = Image.open('banner_top.png')
bottom_image = Image.open('banner_bottom.png')
main_image = Image.open('main_banner.png')

st.image(main_image,use_column_width='always')
st.title("📄 ToDo App 🗣 - Generate Customized To-Do List")
link_url = "https://multi-pdf-chat-7jqbfux5hxqvdjsngoqyay.streamlit.app/"
st.link_button("Click Here",link_url)

st.sidebar.image(top_image,use_column_width='auto')
choice = st.sidebar.selectbox("Menu", ["Create Task ✅","Update Task 👨‍💻","Delete Task ❌", "View Tasks' Status 👨‍💻"])
st.sidebar.image(bottom_image,use_column_width='auto')
create_table()

if choice == "Create Task ✅":
	st.subheader("Add Item")
	col1,col2 = st.columns(2)

	with col1:
		task = st.text_area("Task To Do")

	with col2:
		task_status = st.selectbox("Status",["ToDo","Doing","Done"])
		task_due_date = st.date_input("Due Date")

	if st.button("Add Task"):
		add_data(task,task_status,task_due_date)
		st.success("Added Task \"{}\" ✅".format(task))
		st.balloons()

elif choice == "Update Task 👨‍💻":
	st.subheader("Edit Items")
	with st.expander("Current Data"):
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

	list_of_tasks = [i[0] for i in view_all_task_names()]
	selected_task = st.selectbox("Task",list_of_tasks)
	task_result = get_task(selected_task)

	if task_result:
		task = task_result[0][0]
		task_status = task_result[0][1]
		task_due_date = task_result[0][2]

		col1,col2 = st.columns(2)

		with col1:
			new_task = st.text_area("Task To Do",task)

		with col2:
			new_task_status = st.selectbox(task_status,["To Do","Doing","Done"])
			new_task_due_date = st.date_input(task_due_date)

		if st.button("Update Task 👨‍💻"):
			edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
			st.success("Updated Task \"{}\" ✅".format(task,new_task))

		with st.expander("View Updated Data 💫"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

elif choice == "Delete Task ❌":
	st.subheader("Delete")
	with st.expander("View Data"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

	unique_list = [i[0] for i in view_all_task_names()]
	delete_by_task_name =  st.selectbox("Select Task",unique_list)
	if st.button("Delete ❌"):
		delete_data(delete_by_task_name)
		st.warning("Deleted Task \"{}\" ✅".format(delete_by_task_name))

	with st.expander("View Updated Data 💫"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

else:
	with st.expander("View All 📝"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df.style.applymap(color_df,subset=['Status']))

	st.sidebar.text("Completed Tasks: " + str(completed_tasks))
	if completed_tasks >= 1:
		st.sidebar.success("Badge Reward 🏆: You've completed a tasks!")

