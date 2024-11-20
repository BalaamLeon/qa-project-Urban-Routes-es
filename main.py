from selenium.webdriver.chrome.service import Service

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber "
                            "solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, '//button[text()="Pedir un taxi"]')
    comfort_button = (By.XPATH, '//div[@class="tariff-cards"]//div[@class="tcard"][4]')
    active_tariff = (By.XPATH, '//div[@class="tariff-cards"]//div[@class="tcard active"]//div[@class="tcard-title"]')
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_text = (By.CLASS_NAME, 'np-text')
    phone_number_field = (By.ID, 'phone')
    phone_number_next_button = (By.XPATH, '//div[@class="number-picker open"]//button[text()="Siguiente"]')
    phone_code_field = (By.XPATH, '//div[@class="number-picker open"]//input[@id="code"]')
    phone_code_confirm_button = (By.XPATH, '//div[@class="number-picker open"]//button[text()="Confirmar"]')
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.XPATH, '//div[@class="payment-picker open"]//div[@class="pp-row disabled"]')
    card_number_field = (By.XPATH, '//div[@class="payment-picker open"]//input[@id="number"]')
    card_code_field = (By.XPATH, '//div[@class="payment-picker open"]//input[@id="code"]')
    card_modal_confirm_button = (By.XPATH, '//div[@class="pp-buttons"]//button[@type="submit"]')
    card_modal_close_button = (
        By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    payment_method_text = (By.CLASS_NAME, 'pp-value-text')
    message_field = (By.ID, 'comment')
    requirements_accordion = (By.CLASS_NAME, 'reqs')
    blanket_and_handkerchiefs = (By.XPATH, '//div[text()="Manta y pañuelos"]//..//span[@class="slider round"]')
    blanket_and_handkerchiefs_checkbox = (By.XPATH, '//div[text()="Manta y pañuelos"]//..//input[@type="checkbox"]')
    ice_cream_add_button = (By.XPATH, '//div[text()="Helado"]//..//div[@class="counter-plus"]')
    ice_cream_counter = (By.XPATH, '//div[text()="Helado"]//..//div[@class="counter-value"]')
    call_taxi_smart_button = (By.XPATH, '//button[@class="smart-button"]')
    driver_name = (By.XPATH, '//div[@class="order-button"]//..//div[2]')

    # Utilizar un selector diferente: CSS_SELECTOR
    order_modal = (By.CSS_SELECTOR, '.order')
    order_number = (By.CSS_SELECTOR, '.order-number')

    def __init__(self, driver):
        self.driver = driver

    # Espera a que se cargue la página
    def wait_for_load_page(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.from_field))

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def start_taxi_reservation(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.call_taxi_button))
        self.driver.find_element(*self.call_taxi_button).click()

    def select_comfort_tariff(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.comfort_button))
        self.driver.find_element(*self.comfort_button).click()

    def get_active_tariff(self):
        return self.driver.find_element(*self.active_tariff).text

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def set_phone(self, phone_number):
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.phone_number_button))
        self.driver.find_element(*self.phone_number_button).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_number_field))
        self.set_phone_number(phone_number)
        self.driver.find_element(*self.phone_number_next_button).click()

    def set_phone_code(self, phone_code):
        self.driver.find_element(*self.phone_code_field).send_keys(phone_code)
        self.driver.find_element(*self.phone_code_confirm_button).click()

    def get_phone_text(self):
        return self.driver.find_element(*self.phone_number_text).text

    def set_card_number(self, card_number):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def set_card_code(self, card_code):
        self.driver.find_element(*self.card_code_field).send_keys(card_code)
        self.driver.find_element(*self.card_code_field).send_keys(Keys.TAB)

    def add_card(self, card_number, card_code):
        self.driver.find_element(*self.payment_method_button).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.add_card_button))
        self.driver.find_element(*self.add_card_button).click()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.driver.find_element(*self.card_modal_confirm_button).click()
        self.driver.find_element(*self.card_modal_close_button).click()

    def get_payment_method_text(self):
        return self.driver.find_element(*self.payment_method_text).text

    def set_message(self, message):
        self.driver.find_element(*self.message_field).send_keys(message)

    def get_message(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    def open_requirements_accordion(self):
        requirements_accordion = self.driver.find_element(*self.requirements_accordion)
        if 'open' not in requirements_accordion.get_attribute('class'):
            requirements_accordion.click()

    def toggle_blanket_and_handkerchiefs(self):
        self.open_requirements_accordion()
        blanket_and_handkerchiefs = self.driver.find_element(*self.blanket_and_handkerchiefs)
        self.driver.execute_script("arguments[0].scrollIntoView();", blanket_and_handkerchiefs)
        blanket_and_handkerchiefs.click()

    def get_blanket_and_handkerchiefs_state(self):
        return self.driver.find_element(*self.blanket_and_handkerchiefs_checkbox).is_selected()

    def add_ice_cream(self):
        self.open_requirements_accordion()
        ice_cream_add_button = self.driver.find_element(*self.ice_cream_add_button)
        self.driver.execute_script("arguments[0].scrollIntoView();", ice_cream_add_button)
        ice_cream_add_button.click()
        ice_cream_add_button.click()

    def get_ice_cream_counter_value(self):
        return self.driver.find_element(*self.ice_cream_counter).text

    def call_taxi(self):
        self.driver.find_element(*self.call_taxi_smart_button).click()

    def order_modal_is_open(self):
        return 'shown' in self.driver.find_element(*self.order_modal).get_attribute('class')

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 60).until(expected_conditions.visibility_of_element_located(self.order_number))

    def get_driver_name(self):
        return self.driver.find_element(*self.driver_name).text


class TestUrbanRoutes:
    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        # from selenium.webdriver import DesiredCapabilities
        # capabilities = DesiredCapabilities.CHROME
        # capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        # cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    # Test 1: Configurar la dirección.
    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.wait_for_load_page()
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    # Test 2: Seleccionar la tarifa Comfort.
    def test_select_comfort_tariff(self):
        self.routes_page.start_taxi_reservation()
        self.routes_page.select_comfort_tariff()
        assert self.routes_page.get_active_tariff() == 'Comfort'

    # Test 3: Rellenar el número de teléfono.
    def test_set_phone_number(self):
        phone_number = data.phone_number
        self.routes_page.set_phone(phone_number)
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_phone_code(code)
        assert self.routes_page.get_phone_text() == phone_number

    # Test 4: Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
        card_number = data.card_number
        card_code = data.card_code
        self.routes_page.add_card(card_number, card_code)
        assert self.routes_page.get_payment_method_text() == 'Tarjeta'

    # Test 5: Escribir un mensaje para el controlador.
    def test_set_message_for_driver(self):
        message = data.message_for_driver
        self.routes_page.set_message(message)
        assert self.routes_page.get_message() == message

    # Test 6: Pedir una manta y pañuelos.
    def test_order_blanket_and_handkerchiefs(self):
        self.routes_page.toggle_blanket_and_handkerchiefs()
        assert self.routes_page.get_blanket_and_handkerchiefs_state()

    # Test 7: Pedir 2 helados.
    def test_add_two_ice_cream(self):
        self.routes_page.add_ice_cream()
        assert self.routes_page.get_ice_cream_counter_value() == '2'

    # Test 8: Aparece el modal para buscar un taxi.
    def test_call_taxi_open_modal(self):
        self.routes_page.call_taxi()
        assert self.routes_page.order_modal_is_open()

    # Test 9: Esperar a que aparezca la información del conductor en el modal.
    def test_wait_driver_info(self):
        self.routes_page.wait_for_driver_info()
        assert self.routes_page.get_driver_name() != ''

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
