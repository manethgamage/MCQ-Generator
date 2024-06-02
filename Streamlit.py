import os
import json
import traceback
import pandas as pd
from src.mcqGenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqGenerator.MCQGenerator import generate_evaluate_chain
from src.mcqGenerator.logger import logging

