from ups import RfcUps


class NextUPSSystems(RfcUps):
    def manufacturer(self) -> str:
        return 'NEXT UPS Systems'

    def output_source(self) -> str:
        """
        NextUPSSystems::upsOutSource.0
        @return: Output source name
        """
        values = {
            1: 'Other',
            2: 'None',
            3: 'Normal',
            4: 'Bypass',
            5: 'Battery',
            6: 'Booster',
            7: 'Reducer',
            8: 'Battery test',
            9: 'Fault',
            10: 'he eco mode',
            11: 'Converter mode'
        }

        status = self.get('.1.3.6.1.4.1.21111.1.1.5.1.0')
        if status not in values:
            return status
        elif status:
            return values[status]

    def status_messages(self) -> list:
        messages = [self.output_source()]
        battery = self.battery()
        # This UPS has no reliable status message, do some assumptions to find problems
        battery_status = self.battery_status()
        if battery_status != 'Normal':
            messages.append(battery_status)
        elif battery == 0:
            messages.append('Bad/empty battery')
        elif battery <= 20:
            messages.append('Low battery')

        return messages
