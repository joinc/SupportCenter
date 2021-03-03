# -*- coding: utf-8 -*-

import sys
import binascii
from pyasn1_modules import rfc2459, pem
from pyasn1.codec.der import decoder
from datetime import datetime

######################################################################################################################


class CertificateFile:
    cert_full = ''
    cert = ''
    cert_format = ''

    def __init__(self, filename):
        # Проверяем на DER
        file1 = open(filename, "rb")
        substrate = file1.read()
        file1.close()
        b0 = substrate[0]
        b1 = substrate[1]
        # Проверка наличия последовательности 0x30, длина сертификата не может быть меньше 127 байт
        if b0 == 48 and b1 > 128:
            self.cert_format = 'DER'
        else:
            self.cert_format = 'PEM'
            file1 = open(filename, "r")
            idx, substrate = pem.readPemBlocksFromFile(
                file1,
                ('-----BEGIN CERTIFICATE-----', '-----END CERTIFICATE-----')
            )
        file1.close()
        try:
            self.cert_full, rest = decoder.decode(substrate, asn1Spec=rfc2459.Certificate())
            self.cert = self.cert_full["tbsCertificate"]
        except:
            self.cert_format = ''

    def notation_OID(self, oidhex_string) -> str:
        hex_list = []
        for char in range(0, len(oidhex_string), 2):
            hex_list.append(oidhex_string[char] + oidhex_string[char + 1])
        del hex_list[0]
        del hex_list[0]
        oid_str = ''
        for element in range(len(hex_list)):
            hex_list[element] = int(hex_list[element], 16)
        x = int(hex_list[0] / 40)
        y = int(hex_list[0] % 40)
        if x > 2:
            y += (x - 2) * 40
            x = 2
        oid_str += str(x) + '.' + str(y)
        val = 0
        for byte in range(1, len(hex_list)):
            val = ((val << 7) | (hex_list[byte] & 0x7F))
            if (hex_list[byte] & 0x80) != 0x80:
                oid_str += "." + str(val)
                val = 0
        return oid_str

    def subjectSignTool(self):
        if self.cert == '':
            return ''
        for ext in self.cert["extensions"]:
            # Ищем расширение subjectSignTool
            if str(ext['extnID']) == "1.2.643.100.111":
                # Его значение надо возвращать
                if sys.platform != "win32":
                    seek = 4
                else:
                    seek = 4
                seek = seek - 2
                sst = ext['extnValue'][seek:].prettyPrint()
                if len(sst) > 1 and sst[0] == '0' and sst[1] == 'x':
                    sst = binascii.unhexlify(sst[2:])
                    sst = sst.decode('utf-8')
                return (sst)
        return ''

    def issuerSignTool(self):
        if self.cert == '':
            return []
        for ext in self.cert["extensions"]:
            # Ищем расширение subjectSignTool
            if str(ext['extnID']) == "1.2.643.100.112":
                # Его значение надо возвращать
                vv = ext['extnValue']
                of2 = 1
                of1 = vv[of2]
                if of1 > 128:
                    of2 += (of1 - 128)
                of2 += 1
                # Add for 0x30
                of2 += 1
                of1 = vv[of2]
                if of1 > 128:
                    of2 += (of1 - 128)
                    of2 += 1
                # Поля issuerSignTools
                fsbCA = []
                # Длина первого поля
                for j in range(0, 4):
                    ltek = vv[of2 + 0]
                    stek = of2 + 1
                    fsb = vv[stek: stek + ltek]
                    fsb = vv[stek: stek + ltek].prettyPrint()
                    if len(fsb) > 1 and fsb[0] == '0' and fsb[1] == 'x':
                        try:
                            val1 = binascii.unhexlify(fsb[2:])
                            fsb = val1.decode('utf-8')
                        except:
                            fsb = vv[stek: stek + ltek].prettyPrint()
                    fsbCA.append(fsb)
                    of2 += (ltek + 2)
                # Возврат значений issuerSignTools
                return fsbCA
        return []

    def classUser(self):
        if self.cert == '':
            return ''
        for ext in self.cert["extensions"]:
            # Ищем расширение subjectSignTool
            if str(ext['extnID']) == "2.5.29.32":
                print('2.5.29.32')
                # Классы защищенности
                # Переводит из двоичной системы счисления (2) в hex
                kc = ext['extnValue'].prettyPrint()
                #                print(kc)
                # Сдвиг на 0x
                kc_hex = kc[2:]
                # 4 - длина заголовка
                kc_hex = kc_hex[4:]
                i32 = kc_hex.find('300806062a85036471')
                tmp_kc = ''
                while i32 != -1:
                    # '300806062a85036471' - 10 байт бинарных и 20 hex-овых; 4 - это 3008
                    kcc_tek = kc_hex[i32 + 4: i32 + 20]
                    oid_kc = self.notation_OID(kcc_tek)
                    tmp_kc = tmp_kc + oid_kc + ';;'
                    kc_hex = kc_hex[i32 + 20:]
                    i32 = kc_hex.find('300806062a85036471')
                return tmp_kc
        return ''

    def parse_issuer_subject(self, who):
        if self.cert == '':
            return {}
        infoMap = {
            "1.2.840.113549.1.9.2": "unstructuredName",
            "1.2.643.100.1": "OGRN",
            "1.2.643.100.5": "OGRNIP",
            "1.2.643.3.131.1.1": "INN",
            "1.2.643.100.3": "SNILS",
            "2.5.4.3": "CN",
            "2.5.4.4": "SN",
            "2.5.4.5": "serialNumber",
            "2.5.4.42": "GN",
            "1.2.840.113549.1.9.1": "E",
            "2.5.4.7": "L",
            "2.5.4.8": "ST",
            "2.5.4.9": "street",
            "2.5.4.10": "O",
            "2.5.4.11": "OU",
            "2.5.4.12": "title",
            "2.5.4.6": "Country",
        }
        issuer_or_subject = {}
        # Владелец сертификата: 0 - неизвестно 1 - физ.лицо 2 - юр.лицо
        vlad = 0
        vlad_o = 0
        for rdn in self.cert[who][0]:
            if not rdn:
                continue
            oid = str(rdn[0][0])
            value = rdn[0][1]
            # SNILS
            if oid == '1.2.643.100.3':
                vlad = 1
            # OGRN
            elif oid == '1.2.643.100.1':
                vlad = 2
            # O
            elif oid == '2.5.4.10':
                vlad_o = 1
            value = value[2:]
            val = value.prettyPrint()
            if len(val) > 1 and val[0] == '0' and val[1] == 'x':
                try:
                    val1 = binascii.unhexlify(val[2:])
                    value = val1.decode('utf-8')
                except:
                    pass
            try:
                if not infoMap[oid] == "Type":
                    issuer_or_subject[infoMap[oid]] = value
                else:
                    try:
                        issuer_or_subject[infoMap[oid]] += ", %s" % value
                    except KeyError:
                        issuer_or_subject[infoMap[oid]] = value
            except KeyError:
                issuer_or_subject[oid] = value
            if vlad_o == 1:
                vlad = 2
        return issuer_or_subject, vlad

    def issuerCert(self):
        return self.parse_issuer_subject("issuer")

    def subjectCert(self):
        return self.parse_issuer_subject('subject')

    def signatureCert(self):
        if self.cert == '':
            return {}
        algosign = self.cert_full["signatureAlgorithm"]['algorithm']
        kk = self.cert_full["signatureValue"].prettyPrint()
        if kk[-3:-1] == "'B":
            # Избавляемся от "' в начале строки и 'B" и конце строки
            kk = kk[2:-3]
            # Переводит из двоичной системы счисления (2) в целое
            kkh = int(kk, 2)
        # В MS из десятичной системы в целое
        else:
            kkh = int(kk, 10)
        sign_hex = hex(kkh)
        sign_hex = sign_hex.rstrip('L')
        return algosign, sign_hex[2:]

    def publicKey(self):
        if self.cert == '':
            return {}
        pubkey = self.cert['subjectPublicKeyInfo']
        tmp_pk = {}
        ff = pubkey['algorithm']
        algo = ff['algorithm']
        tmp_pk['algo'] = algo
        # Проверка на ГОСТ
        if str(algo).find("1.2.643") == -1:
            return tmp_pk
        param = ff['parameters']
        lh = param.prettyPrint()[2:]
        # Со 2-й по 11 позиции, первые два байта тип и длина hex-oid-а
        l1 = int(lh[7:8], 16)
        lh1 = self.notation_OID(lh[4:4 + 4 + l1 * 2])
        # Длина следующего oid-а
        l2 = int(lh[4 + 4 + l1 * 2 + 3: 4 + 4 + l1 * 2 + 4], 16)
        # oid из hex в точечную форму
        lh2 = self.notation_OID(lh[4 + 4 + l1 * 2:4 + 4 + l1 * 2 + 4 + l2 * 2])
        key_bytes = pubkey['subjectPublicKey']
        # Читаем значение открытого ключа как битовую строку
        kk = key_bytes.prettyPrint()
        if kk[-3:-1] == "'B":
            # Избавляемся от "' в начале строки и 'B" и конце строки
            kk = kk[2:-3]
            # Переводит из двоичной системы счисления (2) в целое
            kkh = int(kk, 2)
        # В MS из десятичной системы в целое
        else:
            kkh = int(kk, 10)
        # Из целого в HEX
        kk_hex = hex(kkh)
        # Значение ключа в hex хранится как 0x440... (длина ключа 512 бит) или 0x48180... (длина ключа 1024 бита)
        if kk_hex[3] == '4':
            kk_hex = kk_hex[5:]
        elif kk_hex[3] == '8':
            kk_hex = kk_hex[7:]
        # Обрезвем концевик
        kk_hex = kk_hex.rstrip('L')
        tmp_pk['curve'] = lh1
        tmp_pk['hash'] = lh2
        tmp_pk['valuepk'] = kk_hex
        return (tmp_pk)

    def prettyPrint(self):
        if self.cert == '':
            return ''
        return self.cert_full.prettyPrint()

    def get_serial_number(self):
        serial = str(hex(self.cert.getComponentByName('serialNumber')))
        # Убираем из серийного номера символ (x) - обозначение шестнадцатеричной строки
        serial = serial[0] + serial[2:]
        return serial

    def validityCert(self):
        valid_cert = self.cert.getComponentByName('validity')
        validity_cert = {}
        not_before = valid_cert.getComponentByName('notBefore')
        not_before = str(not_before.getComponent())
        not_after = valid_cert.getComponentByName('notAfter')
        not_after = str(not_after.getComponent())
        validity_cert['not_before'] = datetime.strptime(not_before, '%y%m%d%H%M%SZ')
        validity_cert['not_after'] = datetime.strptime(not_after, '%y%m%d%H%M%SZ')
        return validity_cert

    def KeyUsage(self):
        X509V3_KEY_USAGE_BIT_FIELDS = (
            'digitalSignature',
            'nonRepudiation',
            'keyEncipherment',
            'dataEncipherment',
            'keyAgreement',
            'keyCertSign',
            'CRLSign',
            'encipherOnly',
            'decipherOnly',
        )
        if self.cert == '':
            return []
        ku = []
        for ext in self.cert["extensions"]:
            # Ищем расширение keyUsage
            if str(ext['extnID']) != "2.5.29.15":
                continue
            print('2.5.29.15')
            os16 = ext['extnValue'].prettyPrint()
            os16 = '0404' + os16[2:]
            os = binascii.unhexlify(os16[0:])
            octet_strings = os
            e, f = decoder.decode(decoder.decode(octet_strings)[0], rfc2459.KeyUsage())
            n = 0
            while n < len(e):
                if e[n]:
                    ku.append(X509V3_KEY_USAGE_BIT_FIELDS[n])
                n += 1
            return ku
        return []
