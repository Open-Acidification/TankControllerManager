class Tank<T1, T2> {
  final T1 name;
  final T2 ip;

  Tank(this.name, this.ip);

  Map toJson() => {
        'name': name,
        'ip': ip,
      };

  Tank.fromJson(Map json)
      : name = json['name'],
        ip = json['ip'];

  @override
  bool operator ==(Object other) => hashCode == other.hashCode;

  @override
  int get hashCode => name.hashCode;
}
