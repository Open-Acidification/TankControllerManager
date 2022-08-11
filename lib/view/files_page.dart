import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/app_data.dart';
// import 'package:downloads_path_provider_28/downloads_path_provider_28.dart';
// import 'package:permission_handler/permission_handler.dart';

class Files extends StatelessWidget {
  const Files({
    Key? key,
    required this.context,
  }) : super(key: key);

  final BuildContext context;

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      child: Consumer<AppData>(
        builder: (context, appData, child) {
          // Replace ListView with ListView.builder() because there may be many files.
          var fileRows = <DataRow>[];
          appData.files.forEach(
            (fileName, fileSize) => fileRows.add(
              DataRow(
                cells: <DataCell>[
                  DataCell(Text(fileName.toString())),
                  DataCell(Container(
                      alignment: const Alignment(1.0, 0.0),
                      child: Text(fileSize.toString().trim()))),
                  // DataCell(Container(
                  //   alignment: const Alignment(1.0, 0.0),
                  //   child: IconButton(
                  //     icon: const Icon(Icons.download),
                  //     onPressed: () async {
                  //       // Map<Permission, PermissionStatus> statuses = await [
                  //       //   Permission.storage,
                  //       //   //add more permission to request here.
                  //       // ].request();
                  //       // if (statuses[Permission.storage]!.isGranted) {
                  //       //   var directory =
                  //       //       await DownloadsPathProvider.downloadsDirectory;
                  //       //   if (directory != null) {
                  //       //     String savePath =
                  //       //         directory.path + fileName.toString();
                  //       //     print(savePath);

                  //       //     try {
                  //       //       await Dio().download("http://", savePath,
                  //       //           onReceiveProgress: (received, total) {
                  //       //         if (total != -1) {
                  //       //           print((received / total * 100)
                  //       //                   .toStringAsFixed(0) +
                  //       //               "%");
                  //       //           // Build progressbar feature here
                  //       //         }
                  //       //       });
                  //       //       print("File is saved to download folder.");
                  //       //     } on DioError catch (e) {
                  //       //       print(e.message);
                  //       //     }
                  //       //   }
                  //       // } else {
                  //       //   print("No permission t read and write.");
                  //       // }
                  //     },
                  //   ),
                  // )),
                ],
              ),
            ),
          );
          return ListView(children: <Widget>[
            DataTable(
              headingRowHeight: 0,
              columns: const <DataColumn>[
                DataColumn(label: Text('File Name')),
                DataColumn(label: Text('File Size')),
                // DataColumn(label: Text('')),
              ],
              rows: fileRows,
            )
          ]);
        },
      ),
    );
  }
}
