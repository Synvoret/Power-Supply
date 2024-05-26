FROM python:2.7.12

WORKDIR /power_supply

COPY power_supply.py power_supply_taurus.py power_supply_taurus_css.css requirements.txt /power_supply/

RUN pip install -r requirements.txt

EXPOSE 10000 8080

CMD ["bash", "-c", "python power_supply.py test && python power_supply_taurus.py"]
