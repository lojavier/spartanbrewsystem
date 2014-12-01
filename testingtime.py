from flask import Flask, render_template
import datetime

now = datetime.datetime.now()
timeString = now.strftime("%H:%M")
