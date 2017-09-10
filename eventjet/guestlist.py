# This file is part of eventjet-tools.
#
# Eventjet-tools is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# eventjet-tools is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# eventjet-tools. If not, see <http://www.gnu.org/licenses/>.
#
#
# Copyright (C)
#   2017 Alexander Haase <ahaase@alexhaase.de>
#

import csv


class GuestList(csv.DictReader):
    """
    Parse the guestlist exported from Eventjet.

    This class is a wrapper arroung :py:class:`csv.DictReader` used for parsing
    the guestlist file and converting its values to a easy to use list of
    dictionaries.
    """

    def __init__(self, f):
        """
        Create a new Guestlist instance with the required parameters needed to
        parse the file.


        :param io.TextIOWrapper f: The file to be opened.
        """
        super().__init__(f, delimiter=';')

    def __next__(self):
        """
        Get the next entry in the guestlist.

        This method gets the next line of the guestlist's CSV file and returns
        the data processed and structured as :py:class:`dict`.


        :return: The next guest in the guestlist.
        :rtype: dict
        """
        # Get the next row of the guestlist's CSV file. A modified dictionary
        # containing the row's fields in structured form will be returned. If
        # neccessary, values will be converted to another datatype.
        row = super().__next__()
        return {
            # Include the personal data of the guest, if this data is available.
            'guest': {
                'salutation': row['Anrede'],
                'name': row['Vorname'],
                'surname': row['Nachname'],
                'company': row['Firma'] if row['Firma'] else None,
                'year_of_birth': (int(row['Geburtsjahr'])
                                  if row['Geburtsjahr'] else None),

                # As the address may not be defined (e.g. if the user registered
                # via a guestlist code), it will be an optional sub-dictionary.
                'address': {
                    'street': row['Stra\xDFe'],
                    'zip': int(row['PLZ']),
                    'city': row['Ort'],
                    'country': row['Land']
                } if row['Stra\xDFe'] else None,
            } if row['Vorname'] else None,

            # Add the guest's contact data. The newsletter key indicates, the
            # user agreed to get newsletters and other information via mail. For
            # compatibility reasons, the optional mobilephone number is prefixed
            # by a single quote, which will be removed.
            'mobile': (row['Handynummer'].replace('\'', '', 1)
                       if row['Handynummer'] else None),
            'email': row['E-Mail'],
            'newsletter': self._to_bool(row['Newsletter']),

            # Add additional data about the event the guest participates and the
            # individual ticket he's using.
            'event': {
                'id': int(row['Event-ID']),
                'name': row['Event'],
                'begin': row['Event-Beginn'],
                'end': row['Event-Ende']
            },
            'ticket': {
                'id': int(row['Ticket ID']),
                'code': row['Ticket'],
                'category': row['Kategorie'],
                'price': {
                    'incl_fee': list(row.items())[16][1],
                    'excl_fee': list(row.items())[17][1]
                },
                'download': row['Download Ticket'],
                'created': row['Uhrzeit'],
                'used': self._to_bool(row['Benutzt'])
            },

            # If the guest ordered the ticket, add additional data about the
            # order, payment and invoice (if it is generated by Eventjet).
            'order': {
                'id': int(row['Order-ID']),
                'payment-id': (int(row['Payment-ID'])
                               if row['Payment-ID'] else None),
                'invoice': {
                    'id': int(row['Rechnungs-Nr']),
                    'download': row['Download Rechnung']
                } if row['Rechnungs-Nr'] else None
            } if row['Order-ID'] else None,

            # If the guest got the ticket with a guestlist-code, add the code
            # used for registration.
            'code': row['Code'] if row['Code'] else None
        }

    @staticmethod
    def _to_bool(value):
        """
        :param str value: The value to be converted

        :return: The converted value.
        :rtype: bool
        """
        return True if value == 'ja' else False
